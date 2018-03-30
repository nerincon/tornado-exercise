function tipCalculate (){
    var totaltip = document.getElementById('tipamount');
    var totalamount = document.getElementById('totalamount');
    var service = document.getElementById('service').value;
    var bill = document.getElementById('bill').value;
    
    if (bill == null || bill == '') {
      totaltip.innerHTML = 'Please enter an amount';
      return false;
    }
    if(isNaN(bill)) {
      totaltip.innerHTML = 'Please enter a number';
      return false;
    }
    if(bill >= 0){
      totaltip.innerHTML = '$' + (bill*service);
      totalamount.innerHTML = '$' + (bill * service + bill)
    }
  }