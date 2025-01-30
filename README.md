# karp-client-py
Karp API Client

## Roadmap

- [ ] Karp Query DSL
  - [ ] Query operators
    - [ ] `contains|<field>|<string>`
    - [ ] `endswith|<field>|<string>`
    - [x] `equals|<field>|<string>`
    - [ ] `exists|<field>`
    - [ ] `freetext|<string>` 
    - [ ] `gt|<field>|<value>` 
    - [ ] `gte|<field>|<value>`
    - [ ] `lt|<field>|<value>`
    - [ ] `lte|<field>|<value>`
    - [ ] `missing|<field>` 
    - [ ] `regexp|<field>|<regex.*>`
    - [ ] `startswith|<field>|<string>`
  - [ ] Logical operators
    - [ ] `not(<expr1>||<expr2>||...)`
    - [ ] `and(<expr1>||<expr2>||...)`
    - [x] `or(<expr1>||<expr2>||...)`
  - [ ] Subqueries
- [ ] API Calls
  - [ ] Querying
    - [x] `/query/{resources}`
    - [ ] `/query/stats/{resources}`
    - [ ] `/query/entries/{resource_id}/{entry_ids}`
  - [ ] Editing
  - [ ] Statistics
  - [ ] History
  - [ ] Resources
  - [ ] Default
