document.addEventListener('DOMContentLoaded', function () {
            UIkit.scroll('a[href^="#"]', { offset: 80 });
            var phoneInput = document.getElementById('phone-mask');
            if(phoneInput) IMask(phoneInput, { mask: '+7 (000) 000-00-00', lazy: false });
        });