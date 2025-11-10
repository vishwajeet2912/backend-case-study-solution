#  Backend Engineering Intern - Case Study Solution

## Candidate
**Name:** Vishwajeet Kadam  
**Role:** Backend Engineering Intern  
**Tech Stack:** Python (Flask), MySQL, SQLAlchemy  

---

## Overview
This repository contains my complete solution for the **Inventory Management System (StockFlow)** backend case study.  
The project covers:
1. Code Review & Debugging  
2. Database Schema Design  
3. Low-Stock Alert API Implementation  

---

## Part 1 – Code Review & Debugging
A previous intern wrote a buggy API endpoint for adding new products.  
I identified logical and technical issues and fixed them.

**Issues Identified:**
-  No input validation  
-  SKU uniqueness not enforced  
-  Two separate commits (risk of partial data)  
-  Missing transaction handling  
-  No error handling or rollback  
-  Missing HTTP status codes  

** Fixed Version:** [`code/create_product_fixed.py`](code/create_product_fixed.py)  
- Added input validation  
- Ensured SKU uniqueness  
- Wrapped in a single transaction  
- Added rollback on failure  
- Proper HTTP responses  

---

##  Part 2 – Database Design
**Key Requirements:**
- Company → multiple warehouses  
- Product → multiple warehouses  
- Track stock history  
- Suppliers supply products  
- Products can be bundles  

**Tables Designed:**
| Table | Key Columns | Notes |
|--------|-------------|-------|
| `companies` | id, name | Each company has many warehouses |
| `warehouses` | id, company_id (FK), name | Belongs to a company |
| `products` | id, sku (unique), name, price, type | `type` = normal/bundle |
| `suppliers` | id, name, email | — |
| `product_suppliers` | product_id, supplier_id | Many-to-many |
| `inventory` | product_id, warehouse_id, quantity | Composite PK (product_id, warehouse_id) |
| `inventory_history` | id, product_id, change, timestamp | Tracks changes |
| `bundle_items` | parent_product_id, child_product_id, quantity | For bundled products |

**Indexes & Constraints:**
- `sku` → UNIQUE index  
- Composite primary key on `(product_id, warehouse_id)`  
- Foreign keys for relational integrity  
Questions for Product Team:
1. Is the stock threshold stored per product or globally?  
2. Should bundles auto-update stock based on components?  
3. Should inventory changes track reasons (sale, return, adjustment)?  
4. Can suppliers serve multiple companies?

---

## Part 3 – API for Low-Stock Alerts

**Endpoint:**
