document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.flash-container .alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.classList.add('alert-saliendo');
            setTimeout(function () {
                alert.remove();
            }, 500);
        }, 3000);
    });
});