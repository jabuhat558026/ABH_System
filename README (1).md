# Abuhat Boarding House Management System

A Python desktop application built with Tkinter + SQLite for managing a boarding house.

## Requirements
- Python 3.8+
- Tkinter (included with standard Python)
- No external packages needed

## How to Run
```bash
python main.py
```

## Files
- `main.py`     — Main GUI application (all UI pages, forms, styling)
- `database.py` — All database logic, CRUD operations, SQLite schema
- `abuhat_bhs.db` — Auto-created SQLite database on first run

## Modules
| Module       | Features                                              |
|--------------|-------------------------------------------------------|
| Dashboard    | Stats: rooms, tenants, income, expenses, recent payments |
| Tenants      | Add / Edit / Deactivate / Delete tenant records       |
| Rooms        | Add / Edit / Delete rooms; auto-tracks occupancy      |
| Leases       | Create lease agreements; auto-generates deposit record |
| Payments     | Record rent/deposits; track by tenant and date        |
| Utilities    | Monthly meter readings; auto-computes bill amount     |
| Expenses     | Track repairs, bills, and operational costs           |

## Business Rules Implemented
- One Room → Many Tenants (one active at a time, enforced)
- One Tenant → One Lease Agreement (unique constraint)
- Creating a Lease → Auto-generates Security Deposit payment
- Room Status (Vacant/Occupied) updates automatically with tenants
- Utility Bill = (CurrReading - PrevReading) × Rate per Unit

## Database Tables
Owner, Room, Tenant, Lease, Payment, Utility, Expense
