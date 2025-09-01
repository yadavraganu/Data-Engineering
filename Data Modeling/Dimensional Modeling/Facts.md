# Facts in Data Modelling

In dimensional data modelling, a **fact** represents a measurable, quantitative piece of information that can be analyzed across various business dimensions. Categorizing facts helps designers choose appropriate aggregation strategies and ensures accurate analytical results.

## 1. Additive Facts

Additive facts can be aggregated (summed) across all dimensions without losing meaning. They form the backbone of most business metrics.

- Definition: can be summed up on any dimension  
- Common examples: total revenue, quantity sold, units produced  
- Use case: summing daily sales across stores and products to get a company-wide total

## 2. Semi-Additive Facts

Semi-additive facts support aggregation over some dimensions but not all. They typically represent stateful measures as of a point in time.

- Definition: can be summed across certain dimensions but not across time  
- Common examples: bank account balance, inventory level, headcount  
- Use case: computing average daily inventory level makes sense, but summing balances over time inflates the figure

## 3. Non-Additive Facts

Non-additive facts cannot be meaningfully summed across any dimension. They often represent ratios or percentages.

- Definition: cannot be aggregated using sum (or other additive functions) on any dimension  
- Common examples: profit margin percentage, temperature readings, ratios  
- Use case: averaging profit margins across products requires weighted calculations, not simple summation

## Summary Table

| Fact Type         | Can Sum Over            | Typical Measures                       |
|-------------------|-------------------------|----------------------------------------|
| Additive          | All dimensions          | Revenue, units sold, costs             |
| Semi-Additive     | Some (excluding time)   | Inventory level, account balance       |
| Non-Additive      | None                    | Ratios, percentages, rates             |
