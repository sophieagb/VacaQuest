document.addEventListener('DOMContentLoaded', function () {
    const rateInputs = document.querySelectorAll('.rate input');

    rateInputs.forEach((input) => {
        input.addEventListener('change', function () {
            // No need for rating text update
        });
    });
});
