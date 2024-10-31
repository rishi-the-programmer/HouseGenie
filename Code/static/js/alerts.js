function showAlert(container,type,message){
    document.querySelector(container).innerHTML=`<div class="alert alert-${type} alert-dismissible fade show" role="alert">${message}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>`;
}

function dismisAlert(container){
    document.querySelector(container).innerHTML='';
}