function updateCategoriesAndServices() {
  var cityId = document.getElementById('city').value;
  var url = '/get_categories_and_services/?city_id=' + cityId;

  fetch(url)
  .then(response => response.json())
  .then(data => {
    var categorySelect = document.getElementById('category');
    categorySelect.innerHTML = '';  // Очистка списка категорий
    var defaultOption = document.createElement('option');
    defaultOption.text = 'Выбрать категорию';
    defaultOption.value = '';
    categorySelect.appendChild(defaultOption);

    data.categories.forEach(category => {
      var option = document.createElement('option');
      option.value = category.id;
      option.text = category.name;
      categorySelect.appendChild(option);
    });

    // Вызовите функцию обновления списка услуг при загрузке категорий
    updateServices(cityId, data.categories[0].id);  // Выберите первую категорию по умолчанию
  });
}

// Вызовите функцию при изменении выбранного города
document.getElementById('city').addEventListener('change', updateCategoriesAndServices);

function updateServices(cityId, categoryId) {
  var url = `/get_categories_and_services/?city_id=${cityId}&category_id=${categoryId}`;

  fetch(url)
  .then(response => response.json())
  .then(data => {
    var serviceSelect = document.getElementById('service');
    serviceSelect.innerHTML = '';  // Очистка списка услуг

    data.services.forEach(service => {
      var option = document.createElement('option');
      option.value = service.id;
      option.text = service.name;
      serviceSelect.appendChild(option);
    });
  });
}

// Вызовите функцию обновления списка услуг при изменении выбранной категории
document.getElementById('category').addEventListener('change', function() {
  var cityId = document.getElementById('city').value;
  var categoryId = document.getElementById('category').value;
  updateServices(cityId, categoryId);
});