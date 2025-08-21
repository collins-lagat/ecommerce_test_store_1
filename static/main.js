function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

class Cart {
  sync() {
    fetch("/api/cart/")
      .then((response) => response.json())
      .then((data) => {
        const count = data.item_set.reduce((acc, item) => acc + item.quantity, 0);

        const cartBadge = document.querySelector("#cart");
        cartBadge.textContent = count;
      });
  }

  addItem(item) {
    fetch("/api/cart/item/add/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      mode: "same-origin",
      body: JSON.stringify({
        product: item,
      }),
    })
      .then((response) => {
        if (response.ok) {
          this.sync();
        }
      });
  }

  clear() {
    fetch("/api/cart/", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      mode: "same-origin",
    })
      .then((response) => {
        if (response.ok) {
          window.location.href = "/";
          this.sync();
        }
      });
  }

  complete() {
    fetch("/api/cart/complete/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      mode: "same-origin",
    })
      .then((response) => {
        if (response.ok) {
          window.location.href = "/profile";
          this.sync();
        }
      });
  }
}


const handleAddToCartButton = function (cart, productId) {
  cart.addItem(productId);
};

const handleClearCartButton = function (cart) {
  cart.clear();
};

const handleCheckoutButton = function (cart) {
  cart.complete();
};


document.addEventListener("DOMContentLoaded", function () {
  const cart = new Cart();
  const addToCartButtons = document.querySelectorAll(".add-to-card");
  const clearCartButton = document.querySelector("#clear-cart");
  const checkoutButton = document.querySelector("#checkout");

  clearCartButton?.addEventListener("click", function () {
    handleClearCartButton(cart);
  });

  checkoutButton?.addEventListener("click", function () {
    handleCheckoutButton(cart);
  });

  addToCartButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const productId = button.dataset.productId;
      handleAddToCartButton(cart, productId);
    });
  });
});

