$('.plus-cart').click(function(){
  var id =$(this).attr("pid").toString();
  var eml =this.parentNode.children[2]
  $.ajax({
      type:"GET",
      url:"/pluscart",
      data:{
         prod_id:id
       },
       success:function(data){
           eml.innerText=data.quantity
           document.getElementById("amount").innerText=data.amount
           document.getElementById("amount").innerText=data.totalamount
       }
 })
})


$('.minus-cart').click(function(){
  var id =$(this).attr("pid").toString();
  var eml =this.parentNode.children[2]
  $.ajax({
      type:"GET",
      url:"/minuscart",
      data:{
         prod_id:id
       },
       success:function(data){
           eml.innerText=data.quantity
           document.getElementById("amount").innerText=data.amount
           document.getElementById("amount").innerText=data.totalamount
       }
 })
})

$('.remove-cart').click(function(){
  var id =$(this).attr("pid").toString();
  $.ajax({
      type:"GET",
      url:"/removecart",
      data:{
         prod_id:id
       },
       success:function(data){
           console.log("Delete")
           document.getElementById("amount").innerText=data.amount
           document.getElementById("amount").innerText=data.totalamount
           eml.parentNode.parentNode.parentNode.remove()
       }
 })
})