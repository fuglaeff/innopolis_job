function fillOrderItemCard(data) {
  var itemCard = document.createElement('div');
  itemCard.id = data.orderItemId;

  var itemName = document.createElement('h1');
  itemName.innerText = 'Item name: ' + data.item.name;
  itemName.className = 'item-name';

  var itemDescr = document.createElement('p');
  itemDescr.innerText = 'Item description: ' + data.item.description;
  itemDescr.className = 'item-description';

  var itemQty = document.createElement('p');
  itemQty.innerText = 'qty: ' + data.qty;
  itemQty.className = 'item-qty';

  var itemPrice = document.createElement('p');
  var finalPrice = data.item.priceDetail.finalPrice * data.qty / 100;
  itemPrice.innerText = 'price: ' + finalPrice + ' ' + data.item.currency;
  itemPrice.className = 'item-price';

  var itemDeleteButton = document.createElement('button');
  itemDeleteButton.innerText = 'Delete';
  itemDeleteButton.className = 'item-delete-button';
  itemDeleteButton.id = data.orderItemId;
  itemDeleteButton.onclick = function(){
      fetch('/order/delete/' + data.orderItemId + '/', {method: 'DELETE',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
    }}).then(
      setTimeout(function(){
      window.location.reload();
      }, 500));
  };

  itemCard.append(itemName, itemDescr, itemQty, itemPrice, itemDeleteButton);

  return itemCard;
};


function fillItemCard (data) {
  document.addEventListener("DOMContentLoaded", function(event){
  var itemPage = document.body;
  console.log('123');
  var itemName = document.createElement('h1');
  itemName.innerText = data.name;
  itemName.className = 'item-name';

  var itemDescr = document.createElement('p');
  itemDescr.innerText = 'Item description: ' + data.description;
  itemDescr.className = 'item-description';

  var itemPrice = document.createElement('p');
  itemPrice.innerHTML = 'Price: <s>' + (data.price  / 100) + ' ' + data.currency + '</s>';
  itemPrice.className = 'item-price';

  var itemDiscount = document.createElement('p');
  itemDiscount.innerText = 'Discount: -' + (data.priceDetail.discAllSum  / 100) + ' ' + data.currency + ' ' + data.priceDetail.discAllVal + '%';
  itemDiscount.className = 'item-discount';

  var itemTax = document.createElement('p');
  itemTax.innerText = 'Tax: +' + (data.priceDetail.taxAllSum  / 100) + ' ' + data.currency + ' ' + data.priceDetail.taxAllVal + '%';
  itemTax.className = 'item-tax';

  var itemFinalPrice = document.createElement('p');
  itemFinalPrice.innerText = 'Final price: ' + (data.priceDetail.finalPrice  / 100 ) + ' ' + data.currency;
  itemTax.className = 'item-final-price';

  var itemAddInOrderForm = document.createElement('form');
  itemAddInOrderForm.setAttribute('action', '/order/');
  itemAddInOrderForm.setAttribute('method', 'POST');

  var itemId = document.createElement('input');
  itemId.setAttribute('type', 'hidden');
  itemId.setAttribute('name', 'item_id');
  itemId.setAttribute('value', data.id);

  var itemAddInOrder = document.createElement('button');
  itemAddInOrder.innerText = 'Add to order';
  itemAddInOrder.className = 'add-to-order';
  itemAddInOrder.setAttribute('type', 'submit')

  itemAddInOrderForm.append(itemId, itemAddInOrder);

  itemPage.append(itemName, itemDescr, itemPrice, itemDiscount, itemTax, itemFinalPrice, itemAddInOrderForm);
}
)}