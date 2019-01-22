# Sitetree admin override needs to be moved somewhere else
from sitetree.admin import TreeItemAdmin, TreeAdmin, override_tree_admin, override_item_admin

class CustomTreeItemAdmin(TreeItemAdmin):
    # That will turn a tree item representation from the default variant
    # with collapsible groupings into a flat one.
    fieldsets = None
    fields = ('parent', 'title', 'url')

# Now we tell the SiteTree to replace generic representations with custom.
override_item_admin(CustomTreeItemAdmin)
