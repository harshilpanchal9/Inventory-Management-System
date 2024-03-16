$(document).ready(function() {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var url = '/view-category?csrfmiddlewaretoken=' + csrftoken;
    $.ajax({
        url: url,
        data: {'pageload':"pageload",
            },
        dataType: 'json',
        success: function(data) {
            var cat_cnt = data.category_counter;
            document.getElementById('category_counter').innerHTML = 'Total Categories: ' + cat_cnt;
            var categories = data.categories;
            var html = '';
            if (categories.length == 0){
                html =` <div class="dashboard-social-list" style="display:flex;height: 680px;">
                        <img src="/media/images/others/empty.jpg" alt="Image not available" style="width:700px;height:auto;margin:auto;">
                        </div>
                        `; 
                $('#search-results').html(html);
            }
            else{
                for (var i = 0; i < categories.length; i++) {
                    html += `
                        <li class="list-group-item d-flex align-items-center">
                            <div class="d-flex align-items-center gap-2">
                            <div>
                                <h6 class="mb-0">${categories[i].categoryname}</h6>
                            </div>
                            </div>
                            <div class="ms-auto font-22">
                            <a href="/edit-category?categoryname=${categories[i].categoryname}&categoryId=${categories[i].id}" style="color:#ff007c;">
                                <i class="lni lni-pencil-alt"></i>
                            </a>
                            <a href="#" onclick="setCategoryId(${categories[i].id},'${categories[i].categoryname}')" style="margin-left:10px;" data-bs-toggle="modal" data-bs-target="#exampleModal">
                            <svg width="24" style="color:red;margin-top:-5px;" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                            </a>
                            <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" style="display: none;" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" id="exampleModalLabel">Delete category</h5>
                                            <button type="button" style="font-size:15px;" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body" style="font-size:16px;">Are you sure want to delete this category ?</div>
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
                                                <form method="post" action="/view-category">
                                                    <input type="hidden" class="form-control" id="categoryname" name="categoryname" value="">
                                                    <input type="hidden" class="form-control" id="categoryid" name="categoryid" value="">
                                                    <button type="submit" class="btn btn-primary">Yes</button>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </li>
                        <hr style="margin:0 0;height:0;">
                    `;
                    $('#search-results').html(html);
                }
            }
        }
    });

    // Onkeyup search functionality
    $('#search-input').on('keyup', function() {
        var category_name = $(this).val().trim();
        if (category_name.length > 0) {
            $.ajax({
                url: url,
                data: {'search-input': category_name},
                dataType: 'json',
                success: function(data) {
                    var cat_cnt = data.category_counter;
                    console.log(cat_cnt);
                    document.getElementById('category_counter').innerHTML = 'Total Categories: ' + cat_cnt;
                    var categories = data.categories;
                    var html = '';
                    if(categories.length == 0){
                        var html = '';
                        html +=`<div class="dashboard-social-list" style="display:flex;height: 680px;">
                                <img src="/media/images/others/empty.jpg" alt="Image not available" style="width:700px;height:auto;margin:auto;">
                                </div>
                                `;
                        $('#search-results').html(html);
                    }else{
                        for (var i = 0; i < categories.length; i++) {
                            html += `
                                <li class="list-group-item d-flex align-items-center">
                                    <div class="d-flex align-items-center gap-2">
                                    <div>
                                        <h6 class="mb-0">${categories[i].categoryname}</h6>
                                    </div>
                                    </div>
                                    <div class="ms-auto font-22">
                                    <a href="/edit-category?categoryname=${categories[i].categoryname}" style="color:#ff007c;">
                                        <i class="lni lni-pencil-alt"></i>
                                    </a>
                                    <a href="#" onclick="setCategoryId(${categories[i].id},'${categories[i].categoryname}')" style="margin-left:10px;" data-bs-toggle="modal" data-bs-target="#exampleModal">
                                    <svg width="24" style="color:red;margin-top:-5px;" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                                    </a>
                                    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" style="display: none;" aria-hidden="true">
                                        <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                            <h5 class="modal-title" id="exampleModalLabel">Delete category</h5>
                                            <button type="button" style="font-size:15px;" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body" style="font-size:16px;">Are you sure want to delete this category ?</div>
                                            <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
                                            <form method="post" action="/view-category">
                                                <input type="hidden" class="form-control" id="categoryname" name="categoryname" value="">
                                                <input type="hidden" class="form-control" id="categoryid" name="categoryid" value="">
                                                <button type="submit" class="btn btn-primary">Yes</button>
                                            </form>
                                            </div>
                                        </div>
                                        </div>
                                    </div>
                                    </div>
                                </li>
                                <hr style="margin:0 0;height:0;">
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
                    var cat_cnt = data.category_counter;
                    document.getElementById('category_counter').innerHTML = 'Total Categories: ' + cat_cnt;
                    var categories = data.categories;
                    var html = '';
                    if(categories.length == 0){
                        html =`<div class="dashboard-social-list" style="display:flex;height: 680px;">
                                <img src="/media/images/others/empty.jpg" alt="Image not available" style="width:700px;height:auto;margin:auto;">
                                </div>
                                `;
                        $('#search-results').html(html);
                    }
                    else{
                        for (var i = 0; i < categories.length; i++) {
                            html += `
                                <li class="list-group-item d-flex align-items-center">
                                    <div class="d-flex align-items-center gap-2">
                                    <div>
                                        <h6 class="mb-0">${categories[i].categoryname}</h6>
                                    </div>
                                    </div>
                                    <div class="ms-auto font-22">
                                    <a href="/edit-category?categoryname=${categories[i].categoryname}" style="color:#ff007c;">
                                        <i class="lni lni-pencil-alt"></i>
                                    </a>
                                    <a href="#" onclick="setCategoryId(${categories[i].id},'${categories[i].categoryname}')" style="margin-left:10px;" data-bs-toggle="modal" data-bs-target="#exampleModal">
                                    <svg width="24" style="color:red;margin-top:-5px;" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                                    </a>
                                    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" style="display: none;" aria-hidden="true">
                                        <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                            <h5 class="modal-title" id="exampleModalLabel">Delete category</h5>
                                            <button type="button" style="font-size:15px;" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body" style="font-size:16px;">Are you sure want to delete this category ?</div>
                                            <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
                                            <form method="post" action="/view-category">
                                                <input type="hidden" class="form-control" id="categoryname" name="categoryname" value="">
                                                <input type="hidden" class="form-control" id="categoryid" name="categoryid" value="">
                                                <button type="submit" class="btn btn-primary">Yes</button>
                                            </form>
                                            </div>
                                        </div>
                                        </div>
                                    </div>
                                    </div>
                                </li>
                                <hr style="margin:0 0;height:0;">
                            `;
                            $('#search-results').html(html);
                        }
                    }
                }
            });
        }
    });
});