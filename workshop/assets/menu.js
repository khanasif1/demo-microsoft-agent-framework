// Collapsible menu functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize collapsible sections
    const sectionHeaders = document.querySelectorAll('.nav-section-header');
    
    sectionHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const content = this.nextElementSibling;
            const isCollapsed = content.classList.contains('collapsed');
            
            // Toggle collapsed state
            this.classList.toggle('collapsed');
            content.classList.toggle('collapsed');
            
            // Save state to localStorage
            const sectionId = this.getAttribute('data-section');
            if (sectionId) {
                localStorage.setItem(`nav-section-${sectionId}`, isCollapsed ? 'open' : 'collapsed');
            }
        });
        
        // Restore state from localStorage
        const sectionId = header.getAttribute('data-section');
        if (sectionId) {
            const savedState = localStorage.getItem(`nav-section-${sectionId}`);
            if (savedState === 'collapsed') {
                header.classList.add('collapsed');
                header.nextElementSibling.classList.add('collapsed');
            }
        }
    });
});
