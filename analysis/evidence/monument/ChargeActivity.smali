.class public Lcom/sygame/jingubang/ChargeActivity;
.super Landroid/app/Activity;
.source "ChargeActivity.java"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/sygame/jingubang/ChargeActivity$RechargeWebViewClient;
    }
.end annotation


# instance fields
.field private mBtn:Landroid/widget/Button;

.field private mWebView:Landroid/webkit/WebView;


# direct methods
.method public constructor <init>()V
    .locals 1

    .prologue
    const/4 v0, 0x0

    .line 13
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    .line 14
    iput-object v0, p0, Lcom/sygame/jingubang/ChargeActivity;->mWebView:Landroid/webkit/WebView;

    .line 15
    iput-object v0, p0, Lcom/sygame/jingubang/ChargeActivity;->mBtn:Landroid/widget/Button;

    .line 13
    return-void
.end method

.method private initViews()V
    .locals 5

    .prologue
    const/4 v4, 0x1

    .line 26
    invoke-virtual {p0}, Lcom/sygame/jingubang/ChargeActivity;->getIntent()Landroid/content/Intent;

    move-result-object v0

    .line 27
    .local v0, "intent":Landroid/content/Intent;
    const-string v2, "url"

    invoke-virtual {v0, v2}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 28
    .local v1, "url":Ljava/lang/String;
    sget v2, Lcom/sygame/jingubang/R$id;->charge_btn:I

    invoke-virtual {p0, v2}, Lcom/sygame/jingubang/ChargeActivity;->findViewById(I)Landroid/view/View;

    move-result-object v2

    check-cast v2, Landroid/widget/Button;

    iput-object v2, p0, Lcom/sygame/jingubang/ChargeActivity;->mBtn:Landroid/widget/Button;

    .line 29
    iget-object v2, p0, Lcom/sygame/jingubang/ChargeActivity;->mBtn:Landroid/widget/Button;

    new-instance v3, Lcom/sygame/jingubang/ChargeActivity$1;

    invoke-direct {v3, p0}, Lcom/sygame/jingubang/ChargeActivity$1;-><init>(Lcom/sygame/jingubang/ChargeActivity;)V

    invoke-virtual {v2, v3}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 37
    sget v2, Lcom/sygame/jingubang/R$id;->charge_webview:I

    invoke-virtual {p0, v2}, Lcom/sygame/jingubang/ChargeActivity;->findViewById(I)Landroid/view/View;

    move-result-object v2

    check-cast v2, Landroid/webkit/WebView;

    iput-object v2, p0, Lcom/sygame/jingubang/ChargeActivity;->mWebView:Landroid/webkit/WebView;

    .line 38
    iget-object v2, p0, Lcom/sygame/jingubang/ChargeActivity;->mWebView:Landroid/webkit/WebView;

    invoke-virtual {v2}, Landroid/webkit/WebView;->getSettings()Landroid/webkit/WebSettings;

    move-result-object v2

    invoke-virtual {v2, v4}, Landroid/webkit/WebSettings;->setJavaScriptEnabled(Z)V

    .line 39
    iget-object v2, p0, Lcom/sygame/jingubang/ChargeActivity;->mWebView:Landroid/webkit/WebView;

    invoke-virtual {v2}, Landroid/webkit/WebView;->getSettings()Landroid/webkit/WebSettings;

    move-result-object v2

    invoke-virtual {v2, v4}, Landroid/webkit/WebSettings;->setLoadsImagesAutomatically(Z)V

    .line 40
    iget-object v2, p0, Lcom/sygame/jingubang/ChargeActivity;->mWebView:Landroid/webkit/WebView;

    new-instance v3, Lcom/sygame/jingubang/ChargeActivity$RechargeWebViewClient;

    const/4 v4, 0x0

    invoke-direct {v3, p0, v4}, Lcom/sygame/jingubang/ChargeActivity$RechargeWebViewClient;-><init>(Lcom/sygame/jingubang/ChargeActivity;Lcom/sygame/jingubang/ChargeActivity$RechargeWebViewClient;)V

    invoke-virtual {v2, v3}, Landroid/webkit/WebView;->setWebViewClient(Landroid/webkit/WebViewClient;)V

    .line 41
    iget-object v2, p0, Lcom/sygame/jingubang/ChargeActivity;->mWebView:Landroid/webkit/WebView;

    invoke-virtual {v2, v1}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V

    .line 42
    return-void
.end method


# virtual methods
.method public onConfigurationChanged(Landroid/content/res/Configuration;)V
    .locals 0
    .param p1, "newConfig"    # Landroid/content/res/Configuration;

    .prologue
    .line 66
    invoke-super {p0, p1}, Landroid/app/Activity;->onConfigurationChanged(Landroid/content/res/Configuration;)V

    .line 67
    return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .locals 1
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;

    .prologue
    .line 19
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    .line 21
    sget v0, Lcom/sygame/jingubang/R$layout;->charge_layout:I

    invoke-virtual {p0, v0}, Lcom/sygame/jingubang/ChargeActivity;->setContentView(I)V

    .line 22
    invoke-direct {p0}, Lcom/sygame/jingubang/ChargeActivity;->initViews()V

    .line 23
    return-void
.end method

.method protected onDestroy()V
    .locals 1

    .prologue
    .line 59
    const/4 v0, 0x0

    iput-object v0, p0, Lcom/sygame/jingubang/ChargeActivity;->mWebView:Landroid/webkit/WebView;

    .line 60
    invoke-super {p0}, Landroid/app/Activity;->onDestroy()V

    .line 61
    return-void
.end method

.method public onKeyDown(ILandroid/view/KeyEvent;)Z
    .locals 1
    .param p1, "keyCode"    # I
    .param p2, "event"    # Landroid/view/KeyEvent;

    .prologue
    .line 54
    const/4 v0, 0x1

    return v0
.end method
