# Raft Consensus Algorithm: Step-by-Step Detailed Explanation

Raft is a distributed consensus algorithm that manages a replicated log across a cluster of servers. It guarantees that each server’s state machine processes the same sequence of commands, ensuring strong consistency even in the presence of failures.

## Core Components

- Servers  
  Each node in the cluster runs the Raft protocol and can be in one of three roles: leader, follower, or candidate.

- Terms  
  Raft divides time into terms (monotonically increasing integers). Each term starts with an election; at most one leader is elected per term.

- Log Entries  
  Commands from clients are stored as log entries, each tagged with the term when it was received by the leader.

- Majorities  
  Decisions (like committing entries) require agreement from a majority of servers, ensuring safety despite network partitions or crashes.

## Step-by-Step Workflow

### 1. Leader Election

1. All servers start as followers.  
2. If a follower does not receive heartbeats from a leader within an election timeout, it becomes a candidate and increments its term.  
3. The candidate votes for itself and sends RequestVote RPCs to other servers.  
4. Servers grant their vote if they haven’t voted in this term and the candidate’s log is at least as up-to-date as their own.  
5. If the candidate collects votes from a majority, it becomes leader for the current term and begins sending heartbeats.

### 2. Log Replication

1. Clients send commands to the leader.  
2. The leader appends the command as a new log entry in its own log.  
3. Leader issues AppendEntries RPCs (heartbeats) carrying the new entries to each follower.  
4. Followers append entries to their logs if the previous log index and term match; otherwise they reject and return an error.  
5. Once a new entry is stored on a majority of servers, the leader marks it committed and applies it to its state machine.  
6. The leader returns the result to the client, and followers apply the committed entries in order.

### 3. Safety and Commitment

- **Leader Completeness**  
  A leader for a given term contains all committed entries from previous terms.

- **Log Matching Property**  
  If two logs contain an entry with the same index and term, all preceding entries are identical.

- **Commitment Rule**  
  An entry at term T is considered committed once replicated on a majority in term T (and the leader has advanced to a higher term).

### 4. Log Compaction via Snapshots

- To prevent unbounded log growth, the leader can take periodic snapshots of the state machine.  
- Log entries up to the snapshot’s last included index are discarded.  
- Followers lagging far behind can install the snapshot via InstallSnapshot RPCs.

### 5. Cluster Membership Changes

- Raft uses a two-phase approach (joint consensus):  
  1. Move to an intermediate configuration containing both old and new members.  
  2. Once committed, switch to the new configuration exclusively.  
- This avoids safety violations during membership transitions.

## Detailed Mechanisms

### Terms and Election Timeouts

- Election timeouts are randomized per server to reduce split votes.  
- Terms ensure that outdated leaders step down when they learn of a higher term.

### RequestVote and AppendEntries RPCs

- **RequestVote**  
  Carries candidate’s term, ID, and last log index/term.  

- **AppendEntries**  
  Carries leader’s term, previous log index/term, new entries, and leader’s commit index.  

### Handling Failures

- Followers ignore requests from stale leaders (term checks).  
- Candidates step down if they receive a valid AppendEntries from a current leader.  
- Leaders resign if they discover a higher term in any RPC response.

## When to Use Raft and Trade-Offs

Pros  
- Understandable: Designed to be more readable than Paxos.  
- Leader-centric: Simplifies client interaction (always talk to leader).  
- Strong consistency: Guarantees safety under failures.

Cons  
- Single leader: All writes funnel through one node, creating a potential bottleneck.  
- Latency: Write commits wait for majority acknowledgment.  
- Reconfiguration complexity: Membership changes require careful coordination.

# What Happens When a Raft Node Crashes and Recovers

When a Raft node goes down and later rejoins the cluster, it seamlessly transitions back to follower state, catches up on missed entries (or snapshots), and resumes normal operation without compromising safety or consistency.

## 1. Crash Phase

Before the crash, the node holds:  
- Its persistent state (currentTerm, votedFor, and log entries).  
- A volatile state (commitIndex, lastApplied).  

When it crashes, it simply stops responding to RPCs. The rest of the cluster continues:  
- The leader will note missing AppendEntries responses but still function if it maintains a majority.  
- Followers will continue servicing heartbeats from the leader.

## 2. Restart and Role Initialization

Upon restart, the node:

- Reads its last persistent term and log from disk.  
- Sets itself to follower.  
- Resets its election timeout to a random interval.  

It does **not** immediately become a candidate; it waits for either:

1. Receipt of a valid AppendEntries (heartbeat) from the current leader, or  
2. Election timeout expiry (if leader is unreachable).

## 3. Term and Leader Discovery

- If the current leader is alive, it will send a heartbeat (AppendEntries RPC) before the follower’s election timeout.  
- The recovering follower sees the RPC’s term ≥ its own term, resets its timer, and stays follower.  
- If it sees a higher term in the RPC, it updates its term and clears any votedFor.

## 4. Log Synchronization

The cluster’s leader tracks each follower’s **nextIndex**—the log index it believes the follower needs next. For the recovering node:

1. The leader detects a mismatch between nextIndex and the follower’s last log index.  
2. Leader issues AppendEntries RPCs starting at that nextIndex.  
3. If the follower’s log doesn’t match (term or index mismatch), it rejects.  
4. Leader decrements nextIndex and retries until the follower’s log and the leader’s log agree on the previous entry.  
5. Leader then sends the remaining entries in batch.  
6. Follower appends them and acknowledges.

This catch-up continues until the follower’s log mirrors the leader’s up to leader’s latest commit index.

## 5. Snapshot Installation (if needed)

If the leader has compacted its log and the recovering node’s nextIndex is below the snapshot’s last included index:

1. Leader sends an InstallSnapshot RPC with the snapshot data.  
2. Follower replaces its entire state machine with the snapshot, discards its conflicting log prefix, and installs the snapshot’s last included index and term.  
3. Follower sets its nextIndex = lastIncludedIndex + 1 and continues normal AppendEntries for any new entries beyond the snapshot.

## 6. Committing and Applying Entries

Once the follower’s log catches up:

- The leader includes the follower in majority counts for future commit decisions.  
- Committed entries (up to the cluster’s commitIndex) are applied to the follower’s state machine in order.  

The follower never applies entries out of order, preserving linearizability.

## 7. Resuming Normal Operation

After synchronization:

- The recovering node responds to client queries forwarded by the leader.  
- It participates in elections if it times out without hearing heartbeats.  
- It votes and replicates new entries like any other follower.
