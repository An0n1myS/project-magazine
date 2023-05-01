const loginBtn = document.querySelector('#login-btn');
const registerBtn = document.querySelector('#register-btn');
const loginModal = document.querySelector('#login-modal');
const registerModal = document.querySelector('#register-modal');
const closeLoginModal = document.querySelector('#close-login-btn');
const closeRegisterModal = document.querySelector('#close-registration-btn');

// Переключение на форму авторизации
loginBtn.addEventListener('click', function() {
  loginModal.style.display = 'block';
  registerModal.style.display = 'none';
});
closeLoginModal.addEventListener('click', function() {
  loginModal.style.display = 'none';
});

// Переключение на форму регистрации
registerBtn.addEventListener('click', function() {
  registerModal.style.display = 'block';
  loginModal.style.display = 'none';
});
closeRegisterModal.addEventListener('click', function() {
  registerModal.style.display = 'none';
});




// Example dynamic change of product status
const productCards = document.querySelectorAll('.product-card');

productCards.forEach(card => {
  const statusElement = card.querySelector('.status');
  if (statusElement.textContent == 'In stock') {
    statusElement.classList.remove('out-of-stock');
    statusElement.classList.add('in-stock');
  } else {
    statusElement.classList.remove('in-stock');
    statusElement.classList.add('out-of-stock');
  }
});


function searchAndHighlight(searchTerm) {
  // проверяем, не пустой ли поисковый запрос
  if (!searchTerm || searchTerm.trim().length === 0) {
    return;
  }

  // ищем заданный текст на странице
  var textNodes = document.evaluate(
    "//text()[contains(., '" + searchTerm + "')]",
    document,
    null,
    XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
    null
  );

  // выделяем найденный текст и прокручиваем к нему
  for (var i = 0; i < textNodes.snapshotLength; i++) {
    var textNode = textNodes.snapshotItem(i);
    var spanNode = document.createElement("span");
    spanNode.textContent = textNode.textContent;
    textNode.parentNode.replaceChild(spanNode, textNode);
    spanNode.scrollIntoView();
  }
}

// добавляем обработчик отправки формы
var searchForm = document.querySelector("form[name='search-form']");
searchForm.addEventListener("submit", function(event) {
  // предотвращаем стандартное поведение отправки формы
  event.preventDefault();

  // получаем значение поля ввода и вызываем функцию поиска и выделения текста на странице
  var searchBox = document.querySelector("input[name='query']");
  searchAndHighlight(searchBox.value);
});
