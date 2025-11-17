// Mobile Menu Handler
document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const hamburger = document.getElementById('hamburger');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    // Check if elements exist (not on login page)
    if (!hamburger || !sidebar || !overlay) {
        return;
    }
    
    // Toggle sidebar
    function toggleSidebar() {
        hamburger.classList.toggle('active');
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
        
        // Prevent body scroll when sidebar is open
        if (sidebar.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }
    
    // Open/close sidebar
    hamburger.addEventListener('click', toggleSidebar);
    
    // Close sidebar when clicking overlay
    overlay.addEventListener('click', toggleSidebar);
    
    // Close sidebar when clicking a nav link (on mobile)
    const navLinks = sidebar.querySelectorAll('.nav-item');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                setTimeout(toggleSidebar, 100);
            }
        });
    });
    
    // Close sidebar on window resize if screen becomes large
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            hamburger.classList.remove('active');
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
});