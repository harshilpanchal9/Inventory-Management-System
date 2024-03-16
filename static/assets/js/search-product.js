$(document).ready(function() {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var url = '/view-products?csrfmiddlewaretoken=' + csrftoken;
    $.ajax({
        url: url,
        data: {'pageload':"pageload",
            },
        dataType: 'json',
        success: function(data) {
            var products = data.products;
            var Category_Data = data.Category_Data;
            var result = "";
            console.log("All products: ",products);
            var html = '';
            if (products.length == 0){
                html =` <tr>
                            <td colspan="11" style="border-bottom:0px;">
                                <img src="/media/images/others/empty-product.png" alt="Image not available" style="width:600px;height:auto;margin:auto;">
                            </td>
                        </tr>
                        `; 
                    $('#search-results').html(html);
            }
            else{
                for (var i = 0; i < products.length; i++) {
                    html += `
                        <tr>`
                            if(typeof products[i].productimage === "undefined" || products[i].productimage === null || products[i].productimage === ""){
                    html += `   <td style="text-align: -webkit-center;">    
                                    <div class="product-img bg-transparent border">
                                        <img src="/media/images/others/shirt.png" width="35" alt="">
                                    </div>
                                </td>
                                `
                            }else{
                    html += `   <td style="text-align: -webkit-center;">    
                                    <div class="product-img bg-transparent border">
                                        <img src="/media/${products[i].productimage}" id="imagename" width="35" alt="">
                                    </div>
                                </td>`
                            }
                    html += `
                            <td>${products[i].productid}</td>
                            <td>${products[i].productname}</td>
                            `
                            for(var j = 0; j < Category_Data.length; j++){
                                if(products[i].category_id == Category_Data[j].id){
                                    result = Category_Data[j].categoryname;
                                    html += `<td>${result}</td>`;
                                }
                            }
                            html += `
                            <td>${products[i].productsize}</td>
                            <td>${products[i].productcolor}</td>
                            <td>${products[i].productmaterial}</td>
                            <td>${products[i].productstock}</td>
                            <td>${products[i].purchaseprice}</td>                                               
                            <td>${products[i].sellprice}</td>                                               
                            <td>
                                <div class="ms-auto font-22 text-primary">
                                    <a href="/edit-product?productimage=${products[i].productimage}&productid=${products[i].productid}&productname=${products[i].productname}&category=${products[i].category_id}&productsize=${products[i].productsize}&productcolor=${products[i].productcolor}&productmaterial=${products[i].productmaterial}&productstock=${products[i].productstock}&purchaseprice=${products[i].purchaseprice}&sellprice=${products[i].sellprice}&productdesc=${products[i].productdesc}" style="color: #ff8b01;">
                                        <i class="lni lni-pencil-alt"></i>
                                    </a>
                                </div>
                            </td>
                            <td>
                                <div class="ms-auto font-22 text-warning">	
                                    <a href="#" onclick="setProductId(${products[i].productid},'${products[i].productname}')" data-bs-toggle="modal" data-bs-target="#exampleModal">
                                    <svg width="24" style="color:red;margin-top:-5px;" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                                    </a>
                                    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" style="display: none;" aria-hidden="true">
                                        <div class="modal-dialog">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                    <h5 class="modal-title" style="color:black;" id="exampleModalLabel">Delete product</h5>
                                                    <button type="button" style="font-size:15px;" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                </div>
                                                <div class="modal-body" style="font-size:16px;color:black;text-align:left;">Are you sure want to delete this product ?</div>
                                                <div class="modal-footer">
                                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
                                                    <form method="post" action="/view-products">
                                                        <input type="hidden" class="form-control" id="productname" name="productname" value="">
                                                        <input type="hidden" class="form-control" id="productid" name="productid" value="">
                                                        <button type="submit" class="btn btn-primary">Yes</button>
                                                    </form>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </td>
                        </tr>
                    `;
                    $('#search-results').html(html);
                }
            }
        }
    });

    // Onkeyup search functionality
    $('#search-input').on('keyup', function() {
        var product_name = $(this).val().trim();
        if (product_name.length > 0) {
            $.ajax({
                url: url,
                data: {'search-input': product_name},
                dataType: 'json',
                success: function(data) {
                    var products = data.products;
                    var Category_Data = data.Category_Data;
                    var result = "";
                    var html = '';
                    if(products.length == 0){
                        var html = '';
                        html +=`<tr>
                                    <td colspan="11" style="border-bottom:0px;">
                                        <img src="/media/images/others/empty-product.png" alt="Image not available" style="width:600px;height:auto;margin:auto;">
                                    </td>
                                </tr>
                                `;
                            $('#search-results').html(html);
                    }else{
                        for (var i = 0; i < products.length; i++) {
                            html += `
                                <tr>`
                                    if(typeof products[i].productimage === "undefined" || products[i].productimage === null || products[i].productimage === ""){
                            html += `   <td style="text-align: -webkit-center;">    
                                            <div class="product-img bg-transparent border">
                                                <img src="/media/images/others/shirt.png" width="35" alt="">
                                            </div>
                                        </td>
                                        `
                                    }else{
                            html += `   <td style="text-align: -webkit-center;">    
                                            <div class="product-img bg-transparent border">
                                                <img src="/media/${products[i].productimage}" id="imagename" width="35" alt="">
                                            </div>
                                        </td>`
                                    }
                            html += `
                                    <td>${products[i].productid}</td>
                                    <td>${products[i].productname}</td>
                                    `
                                        for(var j = 0; j < Category_Data.length; j++){
                                            if(products[i].category_id == Category_Data[j].id){
                                                result = Category_Data[j].categoryname;
                                                html += `<td>${result}</td>`;
                                            }
                                        }
                                    html += `
                                    <td>${products[i].productsize}</td>
                                    <td>${products[i].productcolor}</td>
                                    <td>${products[i].productmaterial}</td>
                                    <td>${products[i].productstock}</td>
                                    <td>${products[i].purchaseprice}</td>                                               
                                    <td>${products[i].sellprice}</td>                                               
                                    <td>
                                        <div class="ms-auto font-22 text-primary">	
                                            <a href="/edit-product?productimage=${products[i].productimage}&productid=${products[i].productid}&productname=${products[i].productname}&category=${products[i].category_id}&productsize=${products[i].productsize}&productcolor=${products[i].productcolor}&productmaterial=${products[i].productmaterial}&productstock=${products[i].productstock}&purchaseprice=${products[i].purchaseprice}&sellprice=${products[i].sellprice}&productdesc=${products[i].productdesc}" style="color: #ff8b01;">
                                                <i class="lni lni-pencil-alt"></i>
                                            </a>
                                        </div>
                                    </td>
                                    <td>
                                        <div class="ms-auto font-22 text-warning">	
                                            <a href="#" onclick="setProductId(${products[i].productid},'${products[i].productname}')" data-bs-toggle="modal" data-bs-target="#exampleModal">
                                            <svg width="24" style="color:red;margin-top:-5px;" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                                            </a>
                                            <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" style="display: none;" aria-hidden="true">
                                                <div class="modal-dialog">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h5 class="modal-title" style="color:black;" id="exampleModalLabel">Delete product</h5>
                                                            <button type="button" style="font-size:15px;" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                        </div>
                                                        <div class="modal-body" style="font-size:16px;color:black;text-align:left;">Are you sure want to delete this product ?</div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
                                                            <form method="post" action="/view-products">
                                                                <input type="hidden" class="form-control" id="productname" name="productname" value="">
                                                                <input type="hidden" class="form-control" id="productid" name="productid" value="">
                                                                <button type="submit" class="btn btn-primary">Yes</button>
                                                            </form>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </td>
                                </tr>
                            `;
                            $('#search-results').html(html);
                        }
                    }
                }
            });
        } else {
            $.ajax({
                url: url,
                data: {'pageload':"pageload"},
                dataType: 'json',
                success: function(data) {
                    var products = data.products;
                    var Category_Data = data.Category_Data;
                    var result = "";
                    var html = '';
                    if(products.length == 0){
                        html +=`<tr>
                                    <td colspan="11" style="border-bottom:0px;">
                                        <img src="/media/images/others/empty-product.png" alt="Image not available" style="width:600px;height:auto;margin:auto;">
                                    </td>
                                </tr>
                                `;
                            $('#search-results').html(html);
                    }
                    else{
                        for (var i = 0; i < products.length; i++) {
                            html += `
                                <tr>`
                                    if(typeof products[i].productimage === "undefined" || products[i].productimage === null || products[i].productimage === ""){
                            html += `   <td style="text-align: -webkit-center;">    
                                            <div class="product-img bg-transparent border">
                                                <img src="/media/images/others/shirt.png" width="35" alt="">
                                            </div>
                                        </td>
                                        `
                                    }else{
                            html += `   <td style="text-align: -webkit-center;">    
                                            <div class="product-img bg-transparent border">
                                                <img src="/media/${products[i].productimage}" id="imagename" width="35" alt="">
                                            </div>
                                        </td>`
                                    }
                            html += `
                                    <td>${products[i].productid}</td>
                                    <td>${products[i].productname}</td>
                                    `
                                    for(var j = 0; j < Category_Data.length; j++){
                                        if(products[i].category_id == Category_Data[j].id){
                                            result = Category_Data[j].categoryname;
                                            html += `<td>${result}</td>`;
                                        }
                                    }
                                    html += `
                                    <td>${products[i].productsize}</td>
                                    <td>${products[i].productcolor}</td>
                                    <td>${products[i].productmaterial}</td>
                                    <td>${products[i].productstock}</td>
                                    <td>${products[i].purchaseprice}</td>                                               
                                    <td>${products[i].sellprice}</td>                                               
                                    <td>
                                        <div class="ms-auto font-22 text-primary">	
                                            <a href="/edit-product?productimage=${products[i].productimage}&productid=${products[i].productid}&productname=${products[i].productname}&category=${products[i].category_id}&productsize=${products[i].productsize}&productcolor=${products[i].productcolor}&productmaterial=${products[i].productmaterial}&productstock=${products[i].productstock}&purchaseprice=${products[i].purchaseprice}&sellprice=${products[i].sellprice}&productdesc=${products[i].productdesc}" style="color: #ff8b01;">
                                                <i class="lni lni-pencil-alt"></i>
                                            </a>
                                        </div>
                                    </td>
                                    <td>
                                        <div class="ms-auto font-22 text-warning">	
                                            <a href="#" onclick="setProductId(${products[i].productid},'${products[i].productname}')" data-bs-toggle="modal" data-bs-target="#exampleModal">
                                            <svg width="24" style="color:red;margin-top:-5px;" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                                            </a>
                                            <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" style="display: none;" aria-hidden="true">
                                                <div class="modal-dialog">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h5 class="modal-title" style="color:black;" id="exampleModalLabel">Delete product</h5>
                                                            <button type="button" style="font-size:15px;" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                        </div>
                                                        <div class="modal-body" style="font-size:16px;color:black;text-align:left;">Are you sure want to delete this product ?</div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
                                                            <form method="post" action="/view-products">
                                                                <input type="hidden" class="form-control" id="productname" name="productname" value="">
                                                                <input type="hidden" class="form-control" id="productid" name="productid" value="">
                                                                <button type="submit" class="btn btn-primary">Yes</button>
                                                            </form>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </td>
                                </tr>
                            `;
                            $('#search-results').html(html);
                        }
                    }
                }
            });
        }
    });
});