.class public Lcom/syyx/sdkproxy/LocalLogin;
.super Ljava/lang/Object;
.implements Ljava/lang/Runnable;
.field public static activity:Landroid/app/Activity;
.field public static dialog:Landroid/app/Dialog;
.field public static switching:Z
.field public token:Ljava/lang/String;
.method public constructor <init>()V
    .locals 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    return-void
.end method
.method public static show(Landroid/app/Activity;)V
    .locals 1
    sput-object p0, Lcom/syyx/sdkproxy/LocalLogin;->activity:Landroid/app/Activity;
    new-instance v0, Lcom/syyx/sdkproxy/LocalLogin;
    invoke-direct {v0}, Lcom/syyx/sdkproxy/LocalLogin;-><init>()V
    invoke-virtual {p0, v0}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V
    return-void
.end method
.method public complete(Ljava/lang/String;)V
    .locals 2
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    new-instance v0, Lcom/syyx/sdkproxy/LocalLogin;
    invoke-direct {v0}, Lcom/syyx/sdkproxy/LocalLogin;-><init>()V
    iput-object p1, v0, Lcom/syyx/sdkproxy/LocalLogin;->token:Ljava/lang/String;
    sget-object v1, Lcom/syyx/sdkproxy/LocalLogin;->activity:Landroid/app/Activity;
    invoke-virtual {v1, v0}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V
    return-void
.end method
.method public run()V
    .locals 5
    iget-object v0, p0, Lcom/syyx/sdkproxy/LocalLogin;->token:Ljava/lang/String;
    if-eqz v0, :show
    invoke-static {}, Landroid/webkit/CookieManager;->getInstance()Landroid/webkit/CookieManager;
    move-result-object v1
    invoke-virtual {v1}, Landroid/webkit/CookieManager;->flush()V
    invoke-static {v0}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->localComplete(Ljava/lang/String;)V
    sget-object v0, Lcom/syyx/sdkproxy/LocalLogin;->dialog:Landroid/app/Dialog;
    invoke-virtual {v0}, Landroid/app/Dialog;->dismiss()V
    return-void
    :show
    sget-object v0, Lcom/syyx/sdkproxy/LocalLogin;->activity:Landroid/app/Activity;
    new-instance v1, Landroid/app/Dialog;
    invoke-direct {v1, v0}, Landroid/app/Dialog;-><init>(Landroid/content/Context;)V
    const/4 v2, 0x1
    invoke-virtual {v1, v2}, Landroid/app/Dialog;->requestWindowFeature(I)Z
    sput-object v1, Lcom/syyx/sdkproxy/LocalLogin;->dialog:Landroid/app/Dialog;
    new-instance v2, Landroid/webkit/WebView;
    invoke-direct {v2, v0}, Landroid/webkit/WebView;-><init>(Landroid/content/Context;)V
    invoke-virtual {v2}, Landroid/webkit/WebView;->getSettings()Landroid/webkit/WebSettings;
    move-result-object v3
    const/4 v4, 0x1
    invoke-virtual {v3, v4}, Landroid/webkit/WebSettings;->setJavaScriptEnabled(Z)V
    const/4 v4, 0x0
    invoke-virtual {v3, v4}, Landroid/webkit/WebSettings;->setAllowFileAccess(Z)V
    invoke-virtual {v3, v4}, Landroid/webkit/WebSettings;->setSavePassword(Z)V
    const-string v3, "LocalGame"
    invoke-virtual {v2, p0, v3}, Landroid/webkit/WebView;->addJavascriptInterface(Ljava/lang/Object;Ljava/lang/String;)V
    const-string v3, "http://127.0.0.1:18770/local-login"
    sget-boolean v4, Lcom/syyx/sdkproxy/LocalLogin;->switching:Z
    if-eqz v4, :load
    const-string v3, "http://127.0.0.1:18770/local-login?switch=1"
    const/4 v4, 0x0
    sput-boolean v4, Lcom/syyx/sdkproxy/LocalLogin;->switching:Z
    :load
    invoke-virtual {v2, v3}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V
    invoke-virtual {v1, v2}, Landroid/app/Dialog;->setContentView(Landroid/view/View;)V
    invoke-virtual {v1}, Landroid/app/Dialog;->show()V
    invoke-virtual {v1}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;
    move-result-object v2
    const/4 v3, -0x1
    invoke-virtual {v2, v3, v3}, Landroid/view/Window;->setLayout(II)V
    return-void
.end method
