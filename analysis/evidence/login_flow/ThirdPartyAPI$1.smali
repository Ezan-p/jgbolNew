.class Lcom/syyx/sdkproxy/ThirdPartyAPI$1;
.super Ljava/lang/Object;
.source "ThirdPartyAPI.java"

# interfaces
.implements Lcom/qihoo/gamecenter/sdk/common/IDispatcherCallback;


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/syyx/sdkproxy/ThirdPartyAPI;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# direct methods
.method constructor <init>()V
    .locals 0

    .prologue
    .line 530
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 1
    return-void
.end method


# virtual methods
.method public onFinished(Ljava/lang/String;)V
    .locals 5
    .param p1, "data"    # Ljava/lang/String;

    .prologue
    const/4 v4, 0x1

    const/4 v3, 0x0

    .line 535
    invoke-static {p1}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->access$0(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_0

    .line 555
    :goto_0
    return-void

    .line 540
    :cond_0
    const-string v0, "xiyouji"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "mLoginCallback, data is "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 541
    invoke-static {v3}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->access$1(Z)V

    .line 542
    const/4 v0, 0x0

    sput-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mQihooUserInfo:Lcom/syyx/sdkproxy/QihooUserInfo;

    .line 544
    invoke-static {p1}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->access$2(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    sput-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mAccessToken:Ljava/lang/String;

    .line 546
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mAccessToken:Ljava/lang/String;

    invoke-static {v0}, Landroid/text/TextUtils;->isEmpty(Ljava/lang/CharSequence;)Z

    move-result v0

    if-nez v0, :cond_1

    .line 549
    const-string v0, "xiyouji"

    const-string v1, "ThirdPartyCallback.LOGIN_EVENT, 0"

    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 550
    invoke-static {}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->access$3()Ljava/util/Map;

    move-result-object v0

    const-string v1, "access_token"

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mAccessToken:Ljava/lang/String;

    invoke-interface {v0, v1, v2}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 551
    invoke-static {}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->access$4()Lcom/syyx/sdkproxy/ThirdPartyCallback;

    move-result-object v0

    invoke-interface {v0, v4, v3}, Lcom/syyx/sdkproxy/ThirdPartyCallback;->onEvent(II)V

    goto :goto_0

    .line 553
    :cond_1
    invoke-static {}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->access$5()Landroid/content/Context;

    move-result-object v0

    const-string v1, "get access_token failed!"

    invoke-static {v0, v1, v4}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v0

    invoke-virtual {v0}, Landroid/widget/Toast;->show()V

    goto :goto_0
.end method
