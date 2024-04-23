let gallery = document.querySelector("#products-container-oas")

if (gallery) {
    let product_cards = []
    let prods = get_all_products()
    prods.then(data => {
        for (var i = 0; i < data.count; i++) {
            let prod = data?.products[i]
            let card = `
            <div class="card m-3" style="width: 18rem;">
                <div id="prod-img-${prod.id}"></div>
                <div class="card-body">
                    <h5 class="card-title">${prod.name}</h5>
                    <p class="card-text">${prod.description}</p>
                    <p class="display-5">$ ${prod.original_cost}</p>
                    <button class="btn btn-secondary" id="add-to-cart-${prod.id}" value=${prod.id}>Add to cart</button>
                    <a href="../products/${prod.id}" class="btn btn-primary">View details</a>
                </div>
            </div>
            `
            product_cards.push(card)
        }
        gallery.innerHTML = product_cards


    }).then(() => {
        let imgs = get_all_images()
        imgs.then(res => {
            res.forEach(item => {
                let img_container = document.querySelector(`#prod-img-${item.product_id}`)
                if (img_container) {
                    let temp = `
                <img src="media/${item.images}" height="auto" width="100%" />
                `
                    img_container.innerHTML = temp
                }
                let add_to_cart = document.querySelector(`#add-to-cart-${item.product_id}`)
                if (add_to_cart) {
                    add_to_cart.onclick = (e) => {
                        let temp = add_to_cart_handler(e.target.value)
                        temp.then(res => {
                            window.alert("Product added to cart")
                        })
                    }
                }
            })

            // product_images.push(res)
        })
    })
}

