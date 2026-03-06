function previewAvatar(event) {
    const file = event.target.files[0];

    if (file) {
        // Проверка типа файла
        if (!file.type.match('image.*')) {
            alert('Пожалуйста, выберите файл изображения');
            return;
        }

        // Ограничение по размеру (5 МБ)
        if (file.size > 5 * 1024 * 1024) {
            alert('Файл слишком большой. Максимальный размер — 5 МБ');
            return;
        }

        // Создание превью через FileReader
        const reader = new FileReader();

        reader.onload = function(e) {
            const preview = document.getElementById('avatar-preview');
            preview.src = e.target.result; // Устанавливаем новый источник изображения
            preview.classList.add('avatar-changed'); // Визуальная индикация изменения
        };

        reader.readAsDataURL(file); // Читаем файл как Data URL
    }
}


function resetAvatarPreview() {
    const preview = document.getElementById('avatar-preview');
    preview.src = "{{ user.avatar.url|default:'/static/default-avatar.png' }}";
    preview.classList.remove('avatar-changed');
    document.getElementById('id_avatar').value = ''; // Очищаем поле файла
}