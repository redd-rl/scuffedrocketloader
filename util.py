def format_map(customMap: dict):
    templateGridItem = f"""
    <div class="grid-container">
        <article class="grid-item">
        <a class="grid-item-image">
            <img src="{customMap.get('img')}">
            <h1>
            {customMap.get('name')}
            </h1>
            <p>
            {customMap.get('desc')}
            </p>
        </a>
        <hr style="height:2px;border-width:0;color:black;background-color:black">
        <form action="https://localhost:5757" method="post" target="post-receiver">
            <button class="download-button" name="download" type="submit" value="{customMap.get('download-url')}">
            Download
            </button>
            <button class="load-button" name="load" type="submit" value="{customMap.get('identifier')}">
            Load
            </button>
            <button class="delete-button" name="delete" type="submit" value="{customMap.get('identifier')}">
            Delete
            </button>
        </form> 
        </article>
        </div>
    """
def getBasePage():
    return ["""<link href="https://fonts.googleapis.com/css?family=Lexend" rel='stylesheet'>
<body>
    <div class="grid">
    
    ""","""
   
   
   
 <iframe class="post-receiver" name="post-receiver" width="0" height="0" style="display: none;">
 
 </iframe>
</div>
</body>"""]