
/**
 * Dashboard Security and Session Management
 */

class DashboardSecurity {
    constructor() {
        this.sessionCheckInterval = 300000; // 5 minutes
        this.warningTime = 600000; // 10 minutes before expiry
        this.init();
    }
    
    init() {
        this.startSessionMonitor();
        this.addSecurityListeners();
        this.preventRightClick();
    }
    
    startSessionMonitor() {
        setInterval(() => {
            this.checkSession();
        }, this.sessionCheckInterval);
    }
    
    async checkSession() {
        try {
            const response = await fetch('/admin/check-session/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                    'Content-Type': 'application/json',
                },
            });
            
            const data = await response.json();
            
            if (!data.authenticated) {
                this.showSessionExpiredModal();
            }
        } catch (error) {
            console.error('Session check failed:', error);
        }
    }
    
    showSessionExpiredModal() {
        const modal = document.createElement('div');
        modal.innerHTML = `
            <div class="modal fade" id="sessionExpiredModal" tabindex="-1" aria-hidden="true" data-bs-backdrop="static">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content border-danger">
                        <div class="modal-header bg-danger text-white">
                            <h5 class="modal-title">
                                <i class="fas fa-exclamation-triangle me-2"></i>Session Expired
                            </h5>
                        </div>
                        <div class="modal-body text-center">
                            <i class="fas fa-clock text-danger mb-3" style="font-size: 3rem;"></i>
                            <h6>Your session has expired for security reasons.</h6>
                            <p class="text-muted">You will be redirected to the login page.</p>
                        </div>
                        <div class="modal-footer justify-content-center">
                            <button type="button" class="btn btn-primary" onclick="window.location.href='/admin/login/'">
                                <i class="fas fa-sign-in-alt me-2"></i>Login Again
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const modalInstance = new bootstrap.Modal(document.getElementById('sessionExpiredModal'));
        modalInstance.show();
        
        // Auto-redirect after 10 seconds
        setTimeout(() => {
            window.location.href = '/admin/login/';
        }, 10000);
    }
    
    addSecurityListeners() {
        // Warn before leaving page with unsaved changes
        window.addEventListener('beforeunload', (e) => {
            const forms = document.querySelectorAll('form');
            let hasChanges = false;
            
            forms.forEach(form => {
                const formData = new FormData(form);
                if (formData.toString() !== '') {
                    hasChanges = true;
                }
            });
            
            if (hasChanges) {
                e.preventDefault();
                e.returnValue = '';
            }
        });
        
        // Auto-save functionality for forms
        this.enableAutoSave();
    }
    
    enableAutoSave() {
        const forms = document.querySelectorAll('form[data-auto-save]');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                input.addEventListener('input', () => {
                    clearTimeout(this.autoSaveTimeout);
                    this.autoSaveTimeout = setTimeout(() => {
                        this.autoSave(form);
                    }, 2000);
                });
            });
        });
    }
    
    async autoSave(form) {
        try {
            const formData = new FormData(form);
            formData.append('auto_save', 'true');
            
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                },
            });
            
            if (response.ok) {
                this.showAutoSaveIndicator();
            }
        } catch (error) {
            console.error('Auto-save failed:', error);
        }
    }
    
    showAutoSaveIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'alert alert-success alert-dismissible fade show position-fixed';
        indicator.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 250px;';
        indicator.innerHTML = `
            <i class="fas fa-check me-2"></i>Auto-saved
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(indicator);
        
        setTimeout(() => {
            indicator.remove();
        }, 3000);
    }
    
    preventRightClick() {
        // Disable right-click on dashboard pages (optional security measure)
        document.addEventListener('contextmenu', (e) => {
            if (window.location.pathname.startsWith('/dashboard/')) {
                e.preventDefault();
            }
        });
        
        // Disable F12, Ctrl+Shift+I, Ctrl+U (optional)
        document.addEventListener('keydown', (e) => {
            if (
                e.key === 'F12' ||
                (e.ctrlKey && e.shiftKey && e.key === 'I') ||
                (e.ctrlKey && e.key === 'u')
            ) {
                e.preventDefault();
            }
        });
    }
    
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
}

// Initialize dashboard security when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.startsWith('/dashboard/')) {
        new DashboardSecurity();
    }
});

// Utility functions for dashboard
window.DashboardUtils = {
    showAlert: function(message, type = 'info') {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alert);
        
        setTimeout(() => {
            alert.remove();
        }, 5000);
    },
    
    confirmAction: function(message, callback) {
        const modal = document.createElement('div');
        modal.innerHTML = `
            <div class="modal fade" id="confirmModal" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-question-circle me-2"></i>Confirm Action
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            ${message}
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-primary" id="confirmBtn">Confirm</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const modalInstance = new bootstrap.Modal(document.getElementById('confirmModal'));
        modalInstance.show();
        
        document.getElementById('confirmBtn').addEventListener('click', () => {
            callback();
            modalInstance.hide();
            modal.remove();
        });
        
        document.getElementById('confirmModal').addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }
};
