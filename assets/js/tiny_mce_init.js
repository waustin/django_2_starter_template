function CustomFileBrowser(field_name, url, type, win) {

    var cmsURL = '/admin/filebrowser/browse/?pop=2';
    cmsURL = cmsURL + '&type=' + type + "&dir=pages";

    tinyMCE.activeEditor.windowManager.open({
        file: cmsURL,
        width: 980,  // Your dimensions may differ - toy around with them!
        height: 500,
        resizable: 'yes',
        scrollbars: 'yes',
        inline: 'no',  // This parameter only has an effect if you use the inlinepopups plugin!
        close_previous: 'no'
    }, {
        window: win,
        input: field_name,
        editor_id: tinyMCE.selectedInstance.editorId
    });
    return false;
}


tinyMCE.init({
    mode: "specific_textareas",
    editor_selector : "mceEditor",
    theme: "advanced",
    language: "en",
    dialog_type: "modal",
    object_resizing: true,
    cleanup_on_startup: false,
	cleanup: true,
    forced_root_block: "p",
    remove_trailing_nbsp: true,
    theme_advanced_toolbar_location: "top",
    theme_advanced_toolbar_align: "left",
    theme_advanced_statusbar_location: "none",
    theme_advanced_buttons1: "formatselect,styleselect,separator,bold,italic,underline,hr,bullist,numlist,undo,redo,link,unlink,image,separator,code,visualchars,fullscreen,pasteword,pastetext,search,replace,charmap",
    theme_advanced_buttons2: "",
    theme_advanced_buttons3: "",
    theme_advanced_path: false,
    theme_advanced_blockformats: "p,h2,h3,h4,blockquote",
    theme_advanced_styles: "[all] clear=clear;[p] image-grid=image-grid;[img] left=left;[img] right=right;[img] center=center",
    width: '100%',
    height: '650',
    plugins: "advimage,advlink,fullscreen,visualchars,paste,media,template,searchreplace,inlinepopups",
    advimage_styles: "Align Left=left;Align Right=right;",
    advlink_styles: "",
    advimage_update_dimensions_onchange: true,
    file_browser_callback: "CustomFileBrowser",
    relative_urls: false,
    inline_styles: false,
    valid_elements : "@[id|class|title],"
			+ "a[rel|rev|charset|hreflang|tabindex|accesskey|type|name|href|target|title|class|onfocus|onblur],"
			+ "strong/b,em/i,"
			+ "-p,-ol,-ul,-li,br,table,tbody,thead,tr,td,th,img[src|alt=|title|width|height],-sub,-sup,hr,"
			+ "-blockquote,-dd,-dl,-dt,cite,abbr,acronym,"
			+ "object[classid|width|height|codebase|*],param[name|value|_value],embed[type|width|height|src|*],"
            + "iframe[src|width|height|frameborder|*],",
    extended_valid_elements: "" +
    "a[name|class|href|target|title|onclick]," +
    "img[class|src|border=0|alt|title|hspace|vspace|width|height|align|name]," +
    "br[class]," +
	"p[class]," +
    "h2[class],h3[class],h4[class]," +
    "ul[class],ol[class],",
	media_skip_plugin_css:  true,
	paste_auto_cleanup_on_paste : true,
	paste_remove_spans: true,
	paste_remove_styles: true,
    paste_remove_styles_if_webkit: true,
    paste_strip_class_attributes: "all",
});
