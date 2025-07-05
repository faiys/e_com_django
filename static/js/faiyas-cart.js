// console.log("Hi Faiyas")

var updatebtn = document.getElementsByClassName('update-cart')

for (var i=0; i<updatebtn.length; i++){
	updatebtn[i].addEventListener('click',function(){
		var productId = this.dataset.product // referense for stor.html data-product
		var action = this.dataset.action
		//Click in store.html in add cart show console
		// console.log('productId:',productId,'action:',action) 
		
		// referense for base.html script tage 
		// console.log('User:',user) 

		if(user == 'AnonymousUser'){
			console.log('Please log in user')
		}else{
			// console.log('user is login ....')
			var url = '/updateitem/'

			//Api from js to view.py 
			fetch(url,{
			 	method: 'POST',
			 	headers :{'Content-Type': 'application/json',
			 			'X-CSRFToken' : csrftoken,
			 		},
			 	body: JSON.stringify({'productId':productId,'action':action})
				}
			)
			.then(response => {
				return response.json()  //Convert response to JSON
			})
			.then(data =>{
				// console.log('data:',data)
				location.reload()
			})
		}
	})
}