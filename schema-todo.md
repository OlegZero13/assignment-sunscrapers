# Database schema
## Table 'Loans'

### `id`
- primary key, (non null)
- autoincrement

### `member_id`
- foreign key -> Borrowers

### `title`
- varchar(256)
- optional
- to lowercase

### `funded_amnt`
- float
- non null
- clip(0, 5e4)

### `total_pymnt`
- float
- non null
- clip(0, 1e5)

### `sub_grade`
- choice field (categorical)
- options: [A-G][1-5]

### `int_rate`
- float
- non null
- clip(0, 32)

### `loan_amnt`
- float
- non null
- clip(0, 5e4)

### `loan_status`
- non null
- categorical

Split into two:
* `loan_status`: (PAID, CURRENT, CHARGED_OFF, LATE1, LATE2, GRACE, DEFAULT)
* `meets_policy`: (True, False)

Develop necessary logic.

### `term`
- non null
- categorical: (36, 60) months


## Table 'Borrowers`
### `member_id`
- primary key
- autoincrement

### `all_util`
- float
- clip(0, 250)
- convert nan -> 0

### `annual_inc`
- float
- clip(0, 1e7)

### `avg_cur_bal`
- float
- clip(0, 1e5)

### `dti`
- float
- clip(0, 100)

### `home_ownership`
- categorical: (MORTGAGE, RENT, OWN, OTHER)
- default: OTHER

### `addr_state`
- categorical (lookup table)

### `zip_code`
- non null
- varchar(3)
- enforce three first digits
- enforce they are digits

### `emp_title`
- null -> empty string
- enforce lowercase
- remove left and right spaces
- impose ascii characters only

### `emp_length`
- non null
- 0 as default
- clip(0, 10)
- integer

