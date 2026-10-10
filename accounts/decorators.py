from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles):
    """
    Role-based access control decorator:
    - Ensures user is logged in.
    - Superusers and staff with is_superuser or is_staff have full access.
    - Admin users (role == 'admin') inherit all permissions across the system.
    - Managers (role == 'manager') inherit staff-level operational access.
    - Checks if user's role is in allowed_roles.
    - If denied, provides friendly user feedback and redirects to their dashboard.
    """
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            user_role = getattr(user, 'role', '') or ('admin' if user.is_superuser else 'staff')

            # 1. Superusers and Django Staff always have unrestricted access
            if user.is_superuser or getattr(user, 'is_staff', False):
                return view_func(request, *args, **kwargs)

            # 2. System Admins have full access to all views
            if user_role == 'admin':
                return view_func(request, *args, **kwargs)

            # 3. Check direct membership in allowed_roles
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # 4. Role Hierarchy: Managers have access to staff-level views
            if user_role == 'manager' and 'staff' in allowed_roles:
                return view_func(request, *args, **kwargs)

            # 5. Access Restricted - Provide clean, informative user feedback
            messages.warning(
                request,
                f"Access Restricted: Your active account role ({user_role.capitalize()}) does not have permission to access that resource."
            )

            # Redirect safely to user's appropriate workspace
            if user_role == 'admin' or user.is_superuser:
                return redirect('admin_dashboard')
            elif user_role == 'manager':
                return redirect('manager_dashboard')
            else:
                return redirect('staff_dashboard')

        return wrapper
    return decorator