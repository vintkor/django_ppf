if (!$) {
    $ = django.jQuery;
}

function hideInputIfFullText(inputField) {
    if ($(inputField).val()) {
        console.log('readonly');
        $(inputField).attr('readonly', true);
    }
}

$(document).ready(function () {

    var vendor_id = $('#id_vendor_id'),
        vendor_name = $('#id_vendor_name');

    hideInputIfFullText(vendor_id);
    hideInputIfFullText(vendor_name);

});
