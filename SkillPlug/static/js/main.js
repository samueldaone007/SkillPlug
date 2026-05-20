document.addEventListener('DOMContentLoaded', () => {
    // Auto-hide toasts
    setTimeout(() => {
        document.querySelectorAll('.toast-autohide').forEach(t => t.classList.add('opacity-0', 'translate-y-2'));
    }, 3000);
});
