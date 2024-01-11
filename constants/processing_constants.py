not_required_tag_list = [
    "header",
    "footer",
    "meta",
    "style",
    "input",
    "script",
    "link",
    "a",
    "li",
    "aside",
    "button",
    "iframe",
    "svg",
    "path",
    "animatetransform",
    "figure",
    "nav",
    "time",
    "noscript",
    "gu-island",
    "fieldset",
    "form",
    "address",  # generally used for authors - not required
    "details",  # not required as mainly gives dates and published summary
    "template",  # no text in it
    "cite",
    "figcaption",  # do not need the caption of image
]

required_tag_list = [
    "title",
    # "h1",
    # "h2",
    # "h3",
    # "h4",
    # "h5",
    # "h6",
    "div",
    "p",
]

unneccessary_content_list = [
    "click to copy",
    "share this article:",
    "recommended stories",
    "rate story",
    "post to twitter",
    "stories you might be interested in",
    "fill in your details",
    ":",
    "log in",
    "sign in",
    "welcome! log in to your account",
    "recover your password",
    "must read",
    "related news",
    "tip us off",
    "other stories you might like",
    "all rights reserved",
    "read more news",
    "share article",
    "copyright",
    "email newsletter",
    "newsletter",
    "you can use write bot to generate ideas, outlines, ad copy, captions, seo meta data, and more",
    "we may earn a commission from links on this page",
    "chevron icon",
    "link icon",
    "save article icon",
    "search icon",
    "related posts",
    "related topics",
    "shutterstock",
    "show more",
    "more on this story",
    "bbc news",
    "sponsored links",
    "from our sponsor",
    "share this story",
    "read more india stories from the bbc",
    "read more stories from the bbc",
    "share this article",
    "share the news",
    "share this video",
    "more from this stream",
    "the verge",
    "more from",
    "|",  # basically never used in maub content
    "/",
    "share subtitles",
    "advertisementadvertisement",  # not taking single because it may be part of main content
    "most viewedmost viewed",
    "getty images",
    "latest comment",
    "post comment",
    "read comments",
    "also read",
    "listen to this article",
    "advertisement",
    "most read",
    "buzzing now",
    "best of express",
    "0000",
    "1.5x",
    "1.8x",
    "most popular",
    "experience your economic times newspaper the digital way!",
    ",",  # removing , to filter the duplicate content which was not happening because of ,
]  # Replace with the content you want to remove
