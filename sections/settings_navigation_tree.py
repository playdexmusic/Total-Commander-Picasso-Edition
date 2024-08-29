from config.shared_imports import *

class SettingsNavigationTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.add_tree_items()

    def add_tree_items(self):
        """Add sections and subsections to the navigation tree."""
        sections = {
            'General': ['Alerts', 'Fonts', 'Language', 'Logs', 'Shortcuts'],
            'View': ['Menu', 'Panel', 'Themes', 'Toolbar', 'UI'],
            'Table': ['Columns', 'Results', 'Search'],
            'Database': ['Directories', 'Extensions', 'Indexes'],  
            'Setup': ['Apps', 'Bookmarks', 'Filters', 'Groups', 'Highlights', 'Nukes', 'Paths', 'Rules', 'Sections', 'Sites', 'Skiplist', 'Tags'],
        }

        self.tree_items = {}

        for section, subsections in sections.items():
            section_item = QTreeWidgetItem([section])
            self.addTopLevelItem(section_item)
            
            for sub_section in subsections:
                sub_item = QTreeWidgetItem([sub_section])
                section_item.addChild(sub_item)
                self.tree_items[sub_section] = sub_item

        logger.info('Tree items added in specified order.')
