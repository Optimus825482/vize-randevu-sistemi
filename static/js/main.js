// Modern Toast Notification System (SweetAlert inspired)

const TOAST_STYLES = {
    success: {
        icon: 'check-circle-fill',
        iconColor: 'text-emerald-400',
        bg: 'bg-gradient-to-r from-emerald-500/20 to-emerald-600/10',
        border: 'border-emerald-500/50',
        progressBar: 'bg-emerald-500'
    },
    danger: {
        icon: 'x-circle-fill',
        iconColor: 'text-red-400',
        bg: 'bg-gradient-to-r from-red-500/20 to-red-600/10',
        border: 'border-red-500/50',
        progressBar: 'bg-red-500'
    },
    warning: {
        icon: 'exclamation-triangle-fill',
        iconColor: 'text-amber-400',
        bg: 'bg-gradient-to-r from-amber-500/20 to-amber-600/10',
        border: 'border-amber-500/50',
        progressBar: 'bg-amber-500'
    },
    info: {
        icon: 'info-circle-fill',
        iconColor: 'text-sky-400',
        bg: 'bg-gradient-to-r from-sky-500/20 to-sky-600/10',
        border: 'border-sky-500/50',
        progressBar: 'bg-sky-500'
    }
};

function resolveAlertPayload(first, second) {
    if (second === undefined) {
        return { type: 'info', message: first ?? '' };
    }

    const known = ['success', 'danger', 'warning', 'info'];
    if (known.includes(first)) {
        return { type: first, message: second ?? '' };
    }
    if (known.includes(second)) {
        return { type: second, message: first ?? '' };
    }
    return { type: 'info', message: second ?? first ?? '' };
}

// Toast container oluştur
function ensureToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'fixed top-4 right-4 z-[10000] flex flex-col gap-3 pointer-events-none';
        container.style.maxWidth = '420px';
        document.body.appendChild(container);
    }
    return container;
}

function showAlert(typeOrMessage, maybeMessage) {
    const { type, message } = resolveAlertPayload(typeOrMessage, maybeMessage);
    const styles = TOAST_STYLES[type] || TOAST_STYLES.info;
    const duration = 4000;

    const container = ensureToastContainer();

    const toast = document.createElement('div');
    toast.className = `pointer-events-auto transform translate-x-[120%] transition-all duration-300 ease-out`;
    
    const toastId = `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    toast.id = toastId;

    toast.innerHTML = `
        <div class="relative overflow-hidden rounded-2xl border ${styles.border} ${styles.bg} backdrop-blur-xl shadow-2xl">
            <div class="flex items-start gap-4 px-5 py-4">
                <div class="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-slate-950/80 text-2xl ring-2 ring-slate-800/50">
                    <i class="bi bi-${styles.icon} ${styles.iconColor}"></i>
                </div>
                <div class="flex-1 min-w-0 pt-1">
                    <p class="text-sm font-semibold text-slate-100 leading-relaxed break-words">${message}</p>
                </div>
                <button type="button" class="close-toast flex-shrink-0 inline-flex h-8 w-8 items-center justify-center rounded-lg border border-slate-700/50 bg-slate-900/50 text-slate-400 transition hover:bg-slate-800 hover:text-slate-200" aria-label="Kapat">
                    <i class="bi bi-x text-lg"></i>
                </button>
            </div>
            <div class="progress-bar h-1 ${styles.progressBar} transition-all duration-[${duration}ms] ease-linear" style="width: 100%;"></div>
        </div>
    `;

    container.appendChild(toast);

    // Animasyonlu giriş
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            toast.classList.remove('translate-x-[120%]');
            toast.classList.add('translate-x-0');
        });
    });

    // Progress bar animasyonu
    const progressBar = toast.querySelector('.progress-bar');
    requestAnimationFrame(() => {
        progressBar.style.width = '0%';
    });

    // Kapat butonu
    const closeBtn = toast.querySelector('.close-toast');
    closeBtn.addEventListener('click', () => removeToast(toast));

    // Otomatik kapat
    const timeoutId = setTimeout(() => removeToast(toast), duration);

    // Hover ile duraklat
    toast.addEventListener('mouseenter', () => {
        clearTimeout(timeoutId);
        progressBar.style.animationPlayState = 'paused';
    });

    toast.addEventListener('mouseleave', () => {
        setTimeout(() => removeToast(toast), 1000);
    });

    return toast;
}

function removeToast(toast) {
    if (!toast || !toast.parentElement) return;

    toast.style.opacity = '0';
    toast.style.transform = 'translateX(120%) scale(0.8)';
    
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
        
        // Container'ı temizle
        const container = document.getElementById('toast-container');
        if (container && container.children.length === 0) {
            container.remove();
        }
    }, 300);
}

// Eski flash mesajları için uyumluluk
const ALERT_STYLES = TOAST_STYLES;

// SweetAlert tarzı modern onay dialogu
function confirmDelete(message) {
    return new Promise((resolve) => {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 z-[10001] flex items-center justify-center p-4 animate-fadeIn';
        modal.style.backgroundColor = 'rgba(15, 23, 42, 0.8)';
        modal.style.backdropFilter = 'blur(8px)';

        modal.innerHTML = `
            <div class="confirm-modal relative max-w-md w-full transform scale-95 opacity-0 transition-all duration-300">
                <div class="rounded-3xl border border-slate-800/80 bg-slate-950/95 shadow-2xl overflow-hidden">
                    <div class="px-8 pt-8 pb-6 text-center">
                        <div class="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-red-500/10 ring-8 ring-red-500/20">
                            <i class="bi bi-exclamation-triangle-fill text-4xl text-red-400"></i>
                        </div>
                        <h3 class="mb-3 text-xl font-bold text-slate-100">Emin misiniz?</h3>
                        <p class="text-sm text-slate-400 leading-relaxed">
                            ${message || 'Bu işlemi gerçekleştirmek istediğinizden emin misiniz? Bu işlem geri alınamaz.'}
                        </p>
                    </div>
                    <div class="flex gap-3 border-t border-slate-800/60 bg-slate-900/50 px-6 py-4">
                        <button class="cancel-btn flex-1 rounded-xl border border-slate-700 bg-slate-800 px-5 py-3 text-sm font-semibold text-slate-200 transition hover:bg-slate-700">
                            <i class="bi bi-x-circle mr-2"></i>İptal
                        </button>
                        <button class="confirm-btn flex-1 rounded-xl border border-red-500/50 bg-red-500/20 px-5 py-3 text-sm font-semibold text-red-200 transition hover:bg-red-500/30">
                            <i class="bi bi-trash mr-2"></i>Evet, Sil
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Animasyon
        requestAnimationFrame(() => {
            const confirmModal = modal.querySelector('.confirm-modal');
            confirmModal.style.transform = 'scale(1)';
            confirmModal.style.opacity = '1';
        });

        const close = (result) => {
            const confirmModal = modal.querySelector('.confirm-modal');
            confirmModal.style.transform = 'scale(0.95)';
            confirmModal.style.opacity = '0';
            modal.style.opacity = '0';
            
            setTimeout(() => {
                modal.remove();
                resolve(result);
            }, 200);
        };

        modal.querySelector('.cancel-btn').addEventListener('click', () => close(false));
        modal.querySelector('.confirm-btn').addEventListener('click', () => close(true));
        modal.addEventListener('click', (e) => {
            if (e.target === modal) close(false);
        });

        document.addEventListener('keydown', function escHandler(e) {
            if (e.key === 'Escape') {
                document.removeEventListener('keydown', escHandler);
                close(false);
            }
        });
    });
}

async function deleteItem(url, successCallback) {
    const confirmed = await confirmDelete();
    if (!confirmed) return;

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('success', data.message);
                if (typeof successCallback === 'function') {
                    successCallback();
                } else {
                    setTimeout(() => window.location.reload(), 1000);
                }
            } else {
                showAlert('danger', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('danger', 'Bir hata oluştu');
        });
}

function updateStatus(url, status, successCallback) {
    const formData = new FormData();
    formData.append('status', status);

    fetch(url, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('success', data.message);
                if (typeof successCallback === 'function') {
                    successCallback();
                } else {
                    setTimeout(() => window.location.reload(), 1000);
                }
            } else {
                showAlert('danger', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('danger', 'Bir hata oluştu');
        });
}

document.addEventListener('DOMContentLoaded', () => {
    const confirmForms = document.querySelectorAll('[data-confirm]');
    confirmForms.forEach(form => {
        form.addEventListener('submit', event => {
            const msg = form.getAttribute('data-confirm');
            if (!confirmDelete(msg)) {
                event.preventDefault();
            }
        });
    });
});

function exportData(format, url) {
    showAlert('info', 'Rapor hazırlanıyor...');
    window.location.href = `${url}?format=${format}`;
}

function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    if (!input || !table) return;

    const filter = (input.value || '').toUpperCase();
    const rows = table.querySelectorAll('tbody tr');

    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        const match = Array.from(cells).some(cell => {
            const text = cell.textContent || cell.innerText || '';
            return text.toUpperCase().includes(filter);
        });
        row.style.display = match ? '' : 'none';
    });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(
        () => showAlert('success', 'Panoya kopyalandı'),
        () => showAlert('danger', 'Kopyalama başarısız')
    );
}

function printPage() {
    window.print();
}

function formatDate(date) {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    return `${day}.${month}.${year}`;
}

function formatDateTime(datetime) {
    const d = new Date(datetime);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    return `${day}.${month}.${year} ${hours}:${minutes}`;
}
