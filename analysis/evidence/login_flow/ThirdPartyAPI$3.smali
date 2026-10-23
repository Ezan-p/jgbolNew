.class Lcom/syyx/sdkproxy/ThirdPartyAPI$3;
.super Ljava/lang/Object;
.source "ThirdPartyAPI.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/syyx/sdkproxy/ThirdPartyAPI;->login()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# direct methods
.method constructor <init>()V
    .locals 0

    .prologue
    .line 192
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 1
    return-void
.end method


# virtual methods
.method public run()V
    .locals 4

    .prologue
    const/4 v3, 0x1

    .line 197
    const-string v1, "xiyouji"

    const-string v2, "360 login begin ---------------   run"

    invoke-static {v1, v2}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 198
    const/16 v1, 0x101

    invoke-static {v3, v3, v1}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->access$6(ZZI)Landroid/content/Intent;

    move-result-object v0

    .line 199
    .local v0, "intent":Landroid/content/Intent;
    invoke-static {}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->access$5()Landroid/content/Context;

    move-result-object v1

    invoke-static {}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->access$7()Lcom/qihoo/gamecenter/sdk/common/IDispatcherCallback;

    move-result-object v2

    invoke-static {v1, v0, v2}, Lcom/qihoo/gamecenter/sdk/matrix/Matrix;->invokeActivity(Landroid/content/Context;Landroid/content/Intent;Lcom/qihoo/gamecenter/sdk/common/IDispatcherCallback;)V

    .line 201
    return-void
.end method
