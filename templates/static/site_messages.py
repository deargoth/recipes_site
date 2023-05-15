from django.utils.translation import gettext as _

# Error messages to all the site
error = {
    'recipe_not_found': _('Recipe not found.'),
    'category_not_found': _('No category with this name was founded.'),
    'already_logged': _("Ops! You're already logged."),
    'login_required': _("Ops! You need to be logged to do this!"),
    'wrong_credentials': _('Your e-mail or password are wrong. Fix them and try again.'),
    'permission_required': _("Ops! You don't have permission to see that."),
    'recipe_with_same_title': _("There is already a recipe with this title"),
    'slug_already_exists': _("This slug it's already in use"),
}

# Success messages to all the site
success = {
    'register_done': _('You have been registered successfully! Now login in your account.'),
    'successful_login': _('You have been login successfully, enjoy our site!'),
    'logout_done': _('You have been successfully disconnected from your account.'),
    'recipe_updated': _('Your recipe was edited successfully!'),
    'recipe_created': _('Your recipe was send to review sucessfully!'),
    'recipe_deleted': _('Your recipe was deleted successfully.'),
    'profile_updated': _('Your profile was updated successfully!'),
}
