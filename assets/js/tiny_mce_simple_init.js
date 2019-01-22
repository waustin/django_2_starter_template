tinyMCE.init({
    mode: "specific_textareas",
    editor_selector : "mceSimple",
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
    theme_advanced_buttons1: "formatselect,bold,italic,underline,bullist,numlist,undo,redo,link,unlink,code,visualchars,fullscreen,pasteword,pastetext,search,replace,charmap",
	theme_advanced_buttons2: "",
    theme_advanced_buttons3: "",
	theme_advanced_blockformats: "p,h2,h3,h4",
    theme_advanced_path: false,
    width: '800',
    height: '300',
	plugins: "advlink,visualchars,paste,searchreplace,inlinepopups",
    relative_urls: false,
    inline_styles: false,
    valid_elements : "@[id|class|title],"
			+ "a[rel|rev|charset|hreflang|tabindex|accesskey|type|name|href|target|title|class],"
			+ "strong/b,em/i,"
			+ "-p,-ol,-ul,-li,br,-sub,-sup,-h2,-h3,-h4,",
    extended_valid_elements: "" + 
    "a[name|class|href|target|title|onclick]," +
    "br[class]," + 
    "-p[class],",
	paste_auto_cleanup_on_paste : true,
	paste_remove_spans: true,
	paste_remove_styles: true,
    paste_remove_styles_if_webkit: true,
    paste_strip_class_attributes: "all",

});
