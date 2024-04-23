

const get_all_products = async () => {
    let req = await fetch('api/product',
        {
            method: "GET",
            credentials: "include",

        })

    let data = await req.json()
    console.log(data)
    return data
}

const get_product_image_with_id = async (prod_id) => {
    let req = await fetch('api/product',
        {
            method: "GET",
            credentials: "include",

        })
    let data = await req.json()
    return data
}

const get_all_images = async () => {
    let req = await fetch('api/product-images/',
        {
            method: "GET",
            credentials: "include",

        })
    let data = await req.json()
    return data
}

const create_product = async (data) => {
    let req = await fetch('api/product',
        {
            method: "POST",
            credentials: "include",

        })
    let d = await req.json()
    return d
}

const add_to_cart_handler = async (prod_id) => {
    let cookie = get_cookies()['oas_access']
    let req = await fetch(`api/cart/${prod_id}`,
        {
            method: "PUT",
            credentials: "include",
            headers: {
                'Authorization': `oas_access ${cookie}`,
                'Accept': 'application/json',
                 'Content-Type': "multipart/form-data"
            },

        })
    let data = await req.json()
    return data
}

let t = get_all_products()
let product_images = []




t.then(temp => {
    let ele = document.querySelector("#product-count")
    if(ele){
        ele.innerHTML = temp?.count
    }
    let product_div = document.querySelector("#products-accordion")
    let products = []
    if(product_div){
        for (let i = 0; i < temp.count; i++) {
            let prod = temp.products[i]
            let item = `
            <div class="accordion-item">
            <h2 class="accordion-header">
                <button class="accordion-button" type="button" data-bs-toggle="collapse"
                    data-bs-target="#${prod?.id}" aria-expanded="true" aria-controls="${prod.id}">
                    <td><div class="h4">${prod.name}</div></td>
                </button>
            </h2>
            <div id="${prod.id}" class="accordion-collapse collapse show" data-bs-parent="#products-accordion">
                <div class="accordion-body">
                    <strong>${prod.description}</strong>
                    <hr/>
    
                    <div class="d-flex align-items-center justifiy-content-between" >
                    
                        <div style="width:90%;padding:3px" class="d-flex align-items-center justify-content-between">
                            <div style="text-align:left">
                            <div>Product Name</div>
                            <div>Original Cost</div>
                            <div>Discount</div>
                            <div>Delivery Charges</div>
                            <div>Making Charges</div>
                            <div>Origin</div>
                            <div><strong>Total Cost</strong></div>
    
                            </div>
                            <div style="text-align:left">
                            <div>${prod.short_name}</div>
                            <div>$ ${prod.original_cost}</div>
                            <div>${prod.discount_percentage} %</div>
                            <div>${prod.making_charges}</div>
                            <div>${prod.origin_country}</div>
                            <div><strong>$ ${+prod.original_cost + +prod.making_charges - (+prod.original_cost / 100) * (+prod.discount_percentage)}</strong></div>
    
                            </div>
                            <div id="image-container-${prod.id}">
                            </div>
                           
    
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `
      
            products.push(item)
        }
        product_div.innerHTML = products
    }
}).then(() => {
    let imgs = get_all_images()
    imgs.then(res => {
        res.forEach(item => {
            let img_container = document.querySelector(`#image-container-${item.product_id}`)
            if(img_container){
                let temp = `
                <img src="media/${item.images}" height="300" width="500" />
                `
                img_container.innerHTML = temp
            }
        })

        // product_images.push(res)
    })
}
)


let saveBtn = document.querySelector("#save-product")
if(saveBtn){

    saveBtn.onclick = () => {
        let name = document.querySelector("#product-name").value
        let descr = document.querySelector("#product-descr").value
        let price = document.querySelector("#product-price").value
        let discount = document.querySelector("#product-discount").value
        let delivery = document.querySelector("#delivery-charges").value
        let making = document.querySelector("#making-charges").value
        let sellerAddress = document.querySelector("#seller-address").value
        let prodImage = document.querySelector("#product-image").value
    
        let data = {
            "name": name,
            "description": descr,
            "original_cost": price,
            "discount_percentage": discount,
            "delivery_charges": delivery,
            "making_charges": making,
            "seller_address": sellerAddress,
            "image": prodImage
        }
        console.log(data)
    
    }
}