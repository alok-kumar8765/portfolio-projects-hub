
# =========================================================
# ROLE-BASED ACCESS CONTROL
# =========================================================

ROLE_PERMISSIONS = {

    # Full system access
    "admin": {"*"},

    # Chief Executive Officer
    "ceo": {
        "dashboard.view",
        "reports.view",
        "finance.view",
        "finance.reports",
        "shipments.view",
        "fleet.view",
        "warehouse.view",
        "customers.view",
        "tracking.view",
        "drivers.view",
        "billing.view",
    },

    # Operations Manager
    "operations_manager": {
        "dashboard.view",
        "shipments.view",
        "shipments.create",
        "shipments.update",
        "tracking.view",
        "fleet.view",
        "fleet.assign",
        "drivers.view",
        "routes.manage",
        "warehouse.view",
    },

    # Fleet Manager
    "fleet_manager": {
        "fleet.view",
        "fleet.create",
        "fleet.update",
        "drivers.view",
        "drivers.manage",
        "maintenance.manage",
        "trips.view",
        "trips.manage",
    },

    # Warehouse Manager
    "warehouse_manager": {
        "warehouse.view",
        "warehouse.manage",
        "inventory.manage",
        "products.manage",
        "stock.manage",
        "transfers.manage",
    },

    # Accountant
    "accountant": {
        "billing.view",
        "billing.manage",
        "finance.view",
        "finance.manage",
        "finance.reports",
        "reports.view",
        "expenses.manage",
        "payments.manage",
        "vendors.manage",
    },

    # HR Manager
    "hr_manager": {
        "drivers.view",
        "drivers.manage",
        "employees.manage",
    },

    # Customer
    "customer": {
        "customer.shipments.view",
        "customer.invoices.view",
    },

    # Standard operator
    "operator": {
        "dashboard.view",
        "shipments.view",
        "shipments.create",
        "tracking.view",
    },
}


# =========================================================
# PERMISSION CHECK
# =========================================================

def has_permission(role, permission):

    if not role or not permission:
        return False

    permissions = ROLE_PERMISSIONS.get(role, set())

    return "*" in permissions or permission in permissions


# =========================================================
# REQUIRE PERMISSION
# =========================================================

def require_permission(role, permission):

    if not has_permission(role, permission):

        raise PermissionError(
            f"Access denied: role '{role}' "
            f"does not have permission '{permission}'."
        )


# =========================================================
# OPTIONAL USER-BASED CHECK
# =========================================================

def require_user_permission(user, permission):

    if not user:
        raise PermissionError("Authentication required.")

    if not user.get("active", True):
        raise PermissionError("User account is inactive.")

    require_permission(
        user.get("role"),
        permission,
    )
