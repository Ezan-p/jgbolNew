.class public Lcom/syyx/sdkproxy/ThirdPartyAPI;
.super Ljava/lang/Object;
.source "ThirdPartyAPI.java"


# static fields
.field protected static final RESPONSE_TYPE_CODE:Ljava/lang/String; = "code"

.field private static ThirdPartyFlag:I

.field protected static mAccessToken:Ljava/lang/String;

.field private static mCurrentBalance:Ljava/lang/String;

.field private static mIsInOffline:Z

.field private static mLoginCallback:Lcom/qihoo/gamecenter/sdk/common/IDispatcherCallback;

.field protected static mQihooUserInfo:Lcom/syyx/sdkproxy/QihooUserInfo;

.field private static m_map:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map",
            "<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field private static m_sContext:Landroid/content/Context;

.field private static m_sEventCallback:Lcom/syyx/sdkproxy/ThirdPartyCallback;

.field private static m_ui_instance:Landroid/app/Activity;


# direct methods
.method static constructor <clinit>()V
    .locals 2

    .prologue
    const/4 v1, 0x0

    .line 45
    new-instance v0, Ljava/util/HashMap;

    invoke-direct {v0}, Ljava/util/HashMap;-><init>()V

    sput-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    .line 47
    const-string v0, "0"

    sput-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mCurrentBalance:Ljava/lang/String;

    .line 48
    sput-object v1, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    .line 49
    sput-object v1, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sEventCallback:Lcom/syyx/sdkproxy/ThirdPartyCallback;

    .line 50
    sput-object v1, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_ui_instance:Landroid/app/Activity;

    .line 51
    const/4 v0, 0x0

    sput-boolean v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mIsInOffline:Z

    .line 53
    sput-object v1, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mAccessToken:Ljava/lang/String;

    .line 62
    const/16 v0, 0x6b

    sput v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->ThirdPartyFlag:I

    .line 530
    new-instance v0, Lcom/syyx/sdkproxy/ThirdPartyAPI$1;

    invoke-direct {v0}, Lcom/syyx/sdkproxy/ThirdPartyAPI$1;-><init>()V

    sput-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mLoginCallback:Lcom/qihoo/gamecenter/sdk/common/IDispatcherCallback;

    .line 42
    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 42
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method static synthetic access$0(Ljava/lang/String;)Z
    .locals 1

    .prologue
    .line 570
    invoke-static {p0}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->isCancelLogin(Ljava/lang/String;)Z

    move-result v0

    return v0
.end method

.method static synthetic access$1(Z)V
    .locals 0

    .prologue
    .line 51
    sput-boolean p0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mIsInOffline:Z

    return-void
.end method

.method static synthetic access$2(Ljava/lang/String;)Ljava/lang/String;
    .locals 1

    .prologue
    .line 558
    invoke-static {p0}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->parseAccessTokenFromLoginResult(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method static synthetic access$3()Ljava/util/Map;
    .locals 1

    .prologue
    .line 45
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    return-object v0
.end method

.method static synthetic access$4()Lcom/syyx/sdkproxy/ThirdPartyCallback;
    .locals 1

    .prologue
    .line 49
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sEventCallback:Lcom/syyx/sdkproxy/ThirdPartyCallback;

    return-object v0
.end method

.method static synthetic access$5()Landroid/content/Context;
    .locals 1

    .prologue
    .line 48
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    return-object v0
.end method

.method static synthetic access$6(ZZI)Landroid/content/Intent;
    .locals 1

    .prologue
    .line 210
    invoke-static {p0, p1, p2}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->getLoginIntent(ZZI)Landroid/content/Intent;

    move-result-object v0

    return-object v0
.end method

.method static synthetic access$7()Lcom/qihoo/gamecenter/sdk/common/IDispatcherCallback;
    .locals 1

    .prologue
    .line 530
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mLoginCallback:Lcom/qihoo/gamecenter/sdk/common/IDispatcherCallback;

    return-object v0
.end method

.method private checkLoginInfo(Lcom/syyx/sdkproxy/QihooUserInfo;)Z
    .locals 3
    .param p1, "info"    # Lcom/syyx/sdkproxy/QihooUserInfo;

    .prologue
    const/4 v0, 0x1

    const/4 v1, 0x0

    .line 700
    sget-boolean v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mIsInOffline:Z

    if-eqz v2, :cond_1

    .line 707
    :cond_0
    :goto_0
    return v0

    .line 703
    :cond_1
    if-eqz p1, :cond_2

    invoke-virtual {p1}, Lcom/syyx/sdkproxy/QihooUserInfo;->isValid()Z

    move-result v2

    if-nez v2, :cond_0

    .line 704
    :cond_2
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    const-string v2, "\u9700\u8981\u767b\u5f55\u624d\u80fd\u6267\u884c\u6b64\u64cd\u4f5c"

    invoke-static {v0, v2, v1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v0

    invoke-virtual {v0}, Landroid/widget/Toast;->show()V

    move v0, v1

    .line 705
    goto :goto_0
.end method

.method public static doTPAction(Ljava/lang/String;Ljava/lang/String;)V
    .locals 3
    .param p0, "act_name"    # Ljava/lang/String;
    .param p1, "param"    # Ljava/lang/String;

    .prologue
    .line 104
    const-string v0, "xiyouji"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "call doTPAction=======["

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "], p=["

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "]"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 105
    const-string v0, "quit"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_0

    .line 107
    invoke-static {}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->onDestroy()V

    .line 121
    :goto_0
    return-void

    .line 109
    :cond_0
    const-string v0, "pay"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1

    .line 111
    invoke-static {}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->pay()V

    goto :goto_0

    .line 113
    :cond_1
    const-string v0, "get_mem_info"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_2

    .line 115
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    invoke-static {v0}, Lorg/cocos2dx/lib/Cocos2dxUtility;->setAndoirdMemInfo(Ljava/util/Map;)V

    goto :goto_0

    .line 119
    :cond_2
    const-string v0, "xiyouji"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "unhandle doTPAction=======["

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "], p=["

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "]"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    goto :goto_0
.end method

.method public static forum()V
    .locals 2

    .prologue
    .line 332
    const-string v0, "xiyouji"

    const-string v1, "call 360 forum"

    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 333
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_ui_instance:Landroid/app/Activity;

    .line 334
    new-instance v1, Lcom/syyx/sdkproxy/ThirdPartyAPI$5;

    invoke-direct {v1}, Lcom/syyx/sdkproxy/ThirdPartyAPI$5;-><init>()V

    .line 333
    invoke-virtual {v0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 351
    return-void
.end method

.method private static getBBSIntent(Z)Landroid/content/Intent;
    .locals 4
    .param p0, "isLandScape"    # Z

    .prologue
    .line 316
    new-instance v0, Landroid/os/Bundle;

    invoke-direct {v0}, Landroid/os/Bundle;-><init>()V

    .line 319
    .local v0, "bundle":Landroid/os/Bundle;
    const-string v2, "screen_orientation"

    invoke-virtual {v0, v2, p0}, Landroid/os/Bundle;->putBoolean(Ljava/lang/String;Z)V

    .line 322
    const-string v2, "function_code"

    const/16 v3, 0x801

    invoke-virtual {v0, v2, v3}, Landroid/os/Bundle;->putInt(Ljava/lang/String;I)V

    .line 324
    new-instance v1, Landroid/content/Intent;

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    const-class v3, Lcom/qihoo/gamecenter/sdk/activity/ContainerActivity;

    invoke-direct {v1, v2, v3}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 325
    .local v1, "intent":Landroid/content/Intent;
    invoke-virtual {v1, v0}, Landroid/content/Intent;->putExtras(Landroid/os/Bundle;)Landroid/content/Intent;

    .line 327
    return-object v1
.end method

.method public static getBalance()Ljava/lang/String;
    .locals 1

    .prologue
    .line 514
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mCurrentBalance:Ljava/lang/String;

    return-object v0
.end method

.method public static getFlag()I
    .locals 1

    .prologue
    .line 66
    sget v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->ThirdPartyFlag:I

    return v0
.end method

.method private static getLoginInfo()V
    .locals 0

    .prologue
    .line 285
    invoke-static {}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->showMMap()V

    .line 286
    return-void
.end method

.method private static getLoginIntent(ZZI)Landroid/content/Intent;
    .locals 5
    .param p0, "isLandScape"    # Z
    .param p1, "isBgTransparent"    # Z
    .param p2, "act_code"    # I

    .prologue
    const/4 v4, 0x1

    const/4 v3, 0x0

    .line 243
    new-instance v0, Landroid/content/Intent;

    sget-object v1, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    const-class v2, Lcom/qihoo/gamecenter/sdk/activity/ContainerActivity;

    invoke-direct {v0, v1, v2}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 246
    .local v0, "intent":Landroid/content/Intent;
    const-string v1, "screen_orientation"

    invoke-virtual {v0, v1, p0}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Z)Landroid/content/Intent;

    .line 249
    const-string v1, "function_code"

    invoke-virtual {v0, v1, p2}, Landroid/content/Intent;->putExtra(Ljava/lang/String;I)Landroid/content/Intent;

    .line 252
    const-string v1, "login_show_close_icon"

    invoke-virtual {v0, v1, v4}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Z)Landroid/content/Intent;

    .line 255
    const-string v1, "support_offline"

    invoke-virtual {v0, v1, v3}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Z)Landroid/content/Intent;

    .line 258
    const-string v1, "show_autologin_switch"

    invoke-virtual {v0, v1, v3}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Z)Landroid/content/Intent;

    .line 261
    const-string v1, "hide_wellcom"

    invoke-virtual {v0, v1, v4}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Z)Landroid/content/Intent;

    .line 273
    const-string v1, "show_dlg_on_failed_autologin"

    invoke-virtual {v0, v1, v3}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Z)Landroid/content/Intent;

    .line 277
    const-string v1, "xiyouji"

    const-string v2, "enter getLoginIntent return intent "

    invoke-static {v1, v2}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 279
    return-object v0
.end method

.method private getRealNameRegisterIntent(ZLjava/lang/String;)Landroid/content/Intent;
    .locals 4
    .param p1, "isLandScape"    # Z
    .param p2, "qihooUserId"    # Ljava/lang/String;

    .prologue
    .line 751
    new-instance v0, Landroid/os/Bundle;

    invoke-direct {v0}, Landroid/os/Bundle;-><init>()V

    .line 753
    .local v0, "bundle":Landroid/os/Bundle;
    const-string v2, "screen_orientation"

    invoke-virtual {v0, v2, p1}, Landroid/os/Bundle;->putBoolean(Ljava/lang/String;Z)V

    .line 756
    const-string v2, "qihoo_user_id"

    invoke-virtual {v0, v2, p2}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 759
    const-string v2, "ui_background_pictrue"

    const-string v3, ""

    invoke-virtual {v0, v2, v3}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 762
    const-string v2, "function_code"

    const/16 v3, 0x104

    invoke-virtual {v0, v2, v3}, Landroid/os/Bundle;->putInt(Ljava/lang/String;I)V

    .line 764
    new-instance v1, Landroid/content/Intent;

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    const-class v3, Lcom/qihoo/gamecenter/sdk/activity/ContainerActivity;

    invoke-direct {v1, v2, v3}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 765
    .local v1, "intent":Landroid/content/Intent;
    invoke-virtual {v1, v0}, Landroid/content/Intent;->putExtras(Landroid/os/Bundle;)Landroid/content/Intent;

    .line 766
    return-object v1
.end method

.method public static getTPValue(Ljava/lang/String;)Ljava/lang/String;
    .locals 3
    .param p0, "key"    # Ljava/lang/String;

    .prologue
    .line 90
    const-string v0, "xiyouji"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "java getTPValue, k=["

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "]"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 91
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    invoke-interface {v0, p0}, Ljava/util/Map;->containsKey(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_0

    .line 93
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    invoke-interface {v0, p0}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/String;

    .line 97
    :goto_0
    return-object v0

    :cond_0
    const-string v0, ""

    goto :goto_0
.end method

.method private getUploadScoreIntent()Landroid/content/Intent;
    .locals 3

    .prologue
    .line 712
    new-instance v0, Landroid/content/Intent;

    invoke-direct {v0}, Landroid/content/Intent;-><init>()V

    .line 728
    .local v0, "intent":Landroid/content/Intent;
    const-string v1, "function_code"

    const/16 v2, 0x204

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->putExtra(Ljava/lang/String;I)Landroid/content/Intent;

    .line 729
    const-string v1, "score"

    const-string v2, ""

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 730
    const-string v1, "topnid"

    const-string v2, ""

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 731
    return-object v0
.end method

.method public static init(Landroid/content/Context;Lcom/syyx/sdkproxy/ThirdPartyCallback;Landroid/app/Activity;)V
    .locals 2
    .param p0, "ctx"    # Landroid/content/Context;
    .param p1, "cb"    # Lcom/syyx/sdkproxy/ThirdPartyCallback;
    .param p2, "ui"    # Landroid/app/Activity;

    .prologue
    .line 126
    const-string v0, "xiyouji"

    const-string v1, "call TP init==============="

    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 127
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    invoke-static {v0}, Lorg/cocos2dx/lib/Cocos2dxUtility;->setAndoirdMemInfo(Ljava/util/Map;)V

    .line 129
    sput-object p0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    .line 130
    sput-object p1, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sEventCallback:Lcom/syyx/sdkproxy/ThirdPartyCallback;

    .line 131
    sput-object p2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_ui_instance:Landroid/app/Activity;

    .line 132
    const/4 v0, 0x0

    sput-boolean v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mIsInOffline:Z

    .line 142
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_ui_instance:Landroid/app/Activity;

    invoke-static {v0}, Lcom/qihoo/gamecenter/sdk/matrix/Matrix;->init(Landroid/app/Activity;)V

    .line 143
    return-void
.end method

.method private static isCancelLogin(Ljava/lang/String;)Z
    .locals 6
    .param p0, "data"    # Ljava/lang/String;

    .prologue
    const/4 v5, -0x1

    const/4 v2, 0x1

    .line 572
    :try_start_0
    new-instance v1, Lorg/json/JSONObject;

    invoke-direct {v1, p0}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    .line 573
    .local v1, "joData":Lorg/json/JSONObject;
    const-string v3, "errno"

    const/4 v4, -0x1

    invoke-virtual {v1, v3, v4}, Lorg/json/JSONObject;->optInt(Ljava/lang/String;I)I

    move-result v0

    .line 574
    .local v0, "errno":I
    if-ne v5, v0, :cond_0

    .line 575
    const-string v3, "xiyouji"

    new-instance v4, Ljava/lang/StringBuilder;

    const-string v5, "isCancelLogin, errno ===="

    invoke-direct {v4, v5}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v4, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    invoke-static {v3, v4}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 576
    sget-object v3, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    const/4 v4, 0x1

    invoke-static {v3, p0, v4}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v3

    invoke-virtual {v3}, Landroid/widget/Toast;->show()V

    .line 577
    sget-object v3, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sEventCallback:Lcom/syyx/sdkproxy/ThirdPartyCallback;

    const/4 v4, 0x1

    const/4 v5, 0x1

    invoke-interface {v3, v4, v5}, Lcom/syyx/sdkproxy/ThirdPartyCallback;->onEvent(II)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 581
    .end local v0    # "errno":I
    .end local v1    # "joData":Lorg/json/JSONObject;
    :goto_0
    return v2

    .line 580
    :catch_0
    move-exception v2

    .line 581
    :cond_0
    const/4 v2, 0x0

    goto :goto_0
.end method

.method public static login()V
    .locals 2

    .prologue
    .line 189
    const-string v0, "xiyouji"

    const-string v1, "360 login begin ---------------"

    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 191
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_ui_instance:Landroid/app/Activity;

    .line 192
    new-instance v1, Lcom/syyx/sdkproxy/ThirdPartyAPI$3;

    invoke-direct {v1}, Lcom/syyx/sdkproxy/ThirdPartyAPI$3;-><init>()V

    .line 191
    invoke-virtual {v0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 205
    const-string v0, "xiyouji"

    const-string v1, "call 360 login over---------------"

    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 206
    return-void
.end method

.method public static onDestroy()V
    .locals 2

    .prologue
    .line 148
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_ui_instance:Landroid/app/Activity;

    .line 149
    new-instance v1, Lcom/syyx/sdkproxy/ThirdPartyAPI$2;

    invoke-direct {v1}, Lcom/syyx/sdkproxy/ThirdPartyAPI$2;-><init>()V

    .line 148
    invoke-virtual {v0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 184
    return-void
.end method

.method public static onGotAuthorizationCode(Ljava/lang/String;)V
    .locals 4
    .param p0, "authorizationCode"    # Ljava/lang/String;

    .prologue
    const/4 v3, 0x1

    .line 590
    const-string v0, "xiyouji"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "onGotAuthorizationCode --> authorizationCode = "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 592
    invoke-static {p0}, Landroid/text/TextUtils;->isEmpty(Ljava/lang/CharSequence;)Z

    move-result v0

    if-eqz v0, :cond_0

    .line 593
    const-string v0, "xiyouji"

    const-string v1, "360 parseAuthorizationCode is null ---------------"

    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 594
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    const-string v1, "\u672a\u80fd\u83b7\u5f97\u767b\u9646\u6388\u6743,\u8bf7\u7a0d\u540e\u91cd\u8bd5\u3002"

    invoke-static {v0, v1, v3}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v0

    invoke-virtual {v0}, Landroid/widget/Toast;->show()V

    .line 595
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sEventCallback:Lcom/syyx/sdkproxy/ThirdPartyCallback;

    invoke-interface {v0, v3, v3}, Lcom/syyx/sdkproxy/ThirdPartyCallback;->onEvent(II)V

    .line 596
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    const-string v1, "client_code"

    const-string v2, ""

    invoke-interface {v0, v1, v2}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 606
    :goto_0
    return-void

    .line 601
    :cond_0
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    const-string v1, "\u6b63\u5728\u8bf7\u6c42\u5e94\u7528\u670d\u52a1\u5668,\u8bf7\u7a0d\u5019......"

    invoke-static {v0, v1, v3}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v0

    invoke-virtual {v0}, Landroid/widget/Toast;->show()V

    .line 602
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    const-string v1, "client_code"

    invoke-interface {v0, v1, p0}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 603
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sEventCallback:Lcom/syyx/sdkproxy/ThirdPartyCallback;

    const/4 v1, 0x0

    invoke-interface {v0, v3, v1}, Lcom/syyx/sdkproxy/ThirdPartyCallback;->onEvent(II)V

    .line 604
    sput-boolean v3, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mIsInOffline:Z

    goto :goto_0
.end method

.method private static parseAccessTokenFromLoginResult(Ljava/lang/String;)Ljava/lang/String;
    .locals 4
    .param p0, "loginRes"    # Ljava/lang/String;

    .prologue
    .line 561
    :try_start_0
    new-instance v2, Lorg/json/JSONObject;

    invoke-direct {v2, p0}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    .line 562
    .local v2, "joRes":Lorg/json/JSONObject;
    const-string v3, "data"

    invoke-virtual {v2, v3}, Lorg/json/JSONObject;->getJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v1

    .line 563
    .local v1, "joData":Lorg/json/JSONObject;
    const-string v3, "access_token"

    invoke-virtual {v1, v3}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object v3

    .line 567
    .end local v1    # "joData":Lorg/json/JSONObject;
    .end local v2    # "joRes":Lorg/json/JSONObject;
    :goto_0
    return-object v3

    .line 564
    :catch_0
    move-exception v0

    .line 565
    .local v0, "e":Ljava/lang/Exception;
    invoke-virtual {v0}, Ljava/lang/Exception;->printStackTrace()V

    .line 567
    const/4 v3, 0x0

    goto :goto_0
.end method

.method private static parseAuthorizationCode(Ljava/lang/String;)Ljava/lang/String;
    .locals 9
    .param p0, "data"    # Ljava/lang/String;

    .prologue
    .line 619
    const/4 v0, 0x0

    .line 620
    .local v0, "authorizationCode":Ljava/lang/String;
    invoke-static {p0}, Landroid/text/TextUtils;->isEmpty(Ljava/lang/CharSequence;)Z

    move-result v6

    if-nez v6, :cond_1

    .line 621
    const/4 v4, 0x0

    .line 623
    .local v4, "isCallbackParseOk":Z
    :try_start_0
    new-instance v5, Lorg/json/JSONObject;

    invoke-direct {v5, p0}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    .line 624
    .local v5, "json":Lorg/json/JSONObject;
    const-string v6, "errno"

    invoke-virtual {v5, v6}, Lorg/json/JSONObject;->getInt(Ljava/lang/String;)I

    move-result v3

    .line 625
    .local v3, "errCode":I
    const-string v6, "xiyouji"

    new-instance v7, Ljava/lang/StringBuilder;

    const-string v8, "errCode ===="

    invoke-direct {v7, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v7, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v7

    invoke-virtual {v7}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v7

    invoke-static {v6, v7}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 626
    if-nez v3, :cond_0

    .line 628
    const-string v6, "data"

    invoke-virtual {v5, v6}, Lorg/json/JSONObject;->getJSONObject(Ljava/lang/String;)Lorg/json/JSONObject;

    move-result-object v1

    .line 629
    .local v1, "content":Lorg/json/JSONObject;
    const-string v6, "xiyouji"

    new-instance v7, Ljava/lang/StringBuilder;

    const-string v8, "content ===="

    invoke-direct {v7, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v7, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object v7

    invoke-virtual {v7}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v7

    invoke-static {v6, v7}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 630
    if-eqz v1, :cond_0

    .line 632
    const-string v6, "code"

    invoke-virtual {v1, v6}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;
    :try_end_0
    .catch Lorg/json/JSONException; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object v0

    .line 633
    const/4 v4, 0x1

    .line 641
    .end local v1    # "content":Lorg/json/JSONObject;
    .end local v3    # "errCode":I
    .end local v5    # "json":Lorg/json/JSONObject;
    :cond_0
    :goto_0
    if-nez v4, :cond_1

    .line 642
    const-string v6, "xiyouji"

    const-string v7, "360 parseAuthorizationCode fail, data error---------------"

    invoke-static {v6, v7}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 643
    sget-object v6, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    const-string v7, "\u767b\u9646\u9a8c\u8bc1\u51fa\u9519,\u89e3\u6790\u6388\u6743\u7801\u5931\u8d25\u3002"

    const/4 v8, 0x1

    invoke-static {v6, v7, v8}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v6

    invoke-virtual {v6}, Landroid/widget/Toast;->show()V

    .line 647
    .end local v4    # "isCallbackParseOk":Z
    :cond_1
    const-string v6, "xiyouji"

    new-instance v7, Ljava/lang/StringBuilder;

    const-string v8, "parseAuthorizationCode="

    invoke-direct {v7, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v7, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v7

    invoke-virtual {v7}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v7

    invoke-static {v6, v7}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 648
    return-object v0

    .line 636
    .restart local v4    # "isCallbackParseOk":Z
    :catch_0
    move-exception v2

    .line 637
    .local v2, "e":Lorg/json/JSONException;
    invoke-virtual {v2}, Lorg/json/JSONException;->printStackTrace()V

    goto :goto_0
.end method

.method public static pay()V
    .locals 3

    .prologue
    .line 365
    const-string v1, "xiyouji"

    const-string v2, "call 360 pay"

    invoke-static {v1, v2}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 368
    :try_start_0
    sget-object v1, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_ui_instance:Landroid/app/Activity;

    .line 369
    new-instance v2, Lcom/syyx/sdkproxy/ThirdPartyAPI$6;

    invoke-direct {v2}, Lcom/syyx/sdkproxy/ThirdPartyAPI$6;-><init>()V

    .line 368
    invoke-virtual {v1, v2}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 382
    .local v0, "e":Ljava/lang/Exception;
    :goto_0
    return-void

    .line 379
    .end local v0    # "e":Ljava/lang/Exception;
    :catch_0
    move-exception v0

    .line 380
    .restart local v0    # "e":Ljava/lang/Exception;
    invoke-virtual {v0}, Ljava/lang/Exception;->printStackTrace()V

    goto :goto_0
.end method

.method public static purchase(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;IILjava/lang/String;Ljava/lang/String;)V
    .locals 2
    .param p0, "order_id"    # Ljava/lang/String;
    .param p1, "strProductName"    # Ljava/lang/String;
    .param p2, "strProductDes"    # Ljava/lang/String;
    .param p3, "nPrice"    # I
    .param p4, "amount"    # I
    .param p5, "call_back_url"    # Ljava/lang/String;
    .param p6, "product_id"    # Ljava/lang/String;

    .prologue
    .line 358
    const-string v0, "xiyouji"

    const-string v1, "call 360 purchase! should call doTPAction(pay, 360)"

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 359
    return-void
.end method

.method protected static purchase_By_infos()V
    .locals 6

    .prologue
    const/4 v5, 0x1

    .line 388
    invoke-static {}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->showMMap()V

    .line 391
    new-instance v0, Landroid/os/Bundle;

    invoke-direct {v0}, Landroid/os/Bundle;-><init>()V

    .line 394
    .local v0, "bundle":Landroid/os/Bundle;
    const-string v2, "screen_orientation"

    invoke-virtual {v0, v2, v5}, Landroid/os/Bundle;->putBoolean(Ljava/lang/String;Z)V

    .line 397
    const-string v3, "access_token"

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    const-string v4, "access_token"

    invoke-interface {v2, v4}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Ljava/lang/String;

    invoke-virtual {v0, v3, v2}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 400
    const-string v3, "qihoo_user_id"

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    const-string v4, "QIHOO_USER_ID"

    invoke-interface {v2, v4}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Ljava/lang/String;

    invoke-virtual {v0, v3, v2}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 403
    const-string v3, "amount"

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    const-string v4, "AMOUNT"

    invoke-interface {v2, v4}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Ljava/lang/String;

    invoke-virtual {v0, v3, v2}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 406
    const-string v3, "rate"

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    const-string v4, "RATE"

    invoke-interface {v2, v4}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Ljava/lang/String;

    invoke-virtual {v0, v3, v2}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 409
    const-string v3, "product_name"

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    const-string v4, "PRODUCT_NAME"

    invoke-interface {v2, v4}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Ljava/lang/String;

    invoke-virtual {v0, v3, v2}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 412
    const-string v3, "product_id"

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    const-string v4, "PRODUCT_ID"

    invoke-interface {v2, v4}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Ljava/lang/String;

    invoke-virtual {v0, v3, v2}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 415
    const-string v3, "notify_uri"

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    const-string v4, "NOTIFY_URI"

    invoke-interface {v2, v4}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Ljava/lang/String;

    invoke-virtual {v0, v3, v2}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 418
    const-string v3, "app_name"

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    const-string v4, "APP_NAME"

    invoke-interface {v2, v4}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Ljava/lang/String;

    invoke-virtual {v0, v3, v2}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 421
    const-string v3, "app_user_name"

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    const-string v4, "APP_USER_NAME"

    invoke-interface {v2, v4}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Ljava/lang/String;

    invoke-virtual {v0, v3, v2}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 425
    const-string v3, "app_user_id"

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    const-string v4, "APP_USER_ID"

    invoke-interface {v2, v4}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Ljava/lang/String;

    invoke-virtual {v0, v3, v2}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 434
    const-string v3, "app_order_id"

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    const-string v4, "APP_ORDER_ID"

    invoke-interface {v2, v4}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Ljava/lang/String;

    invoke-virtual {v0, v3, v2}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 436
    new-instance v1, Landroid/content/Intent;

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    const-class v3, Lcom/qihoo/gamecenter/sdk/activity/ContainerActivity;

    invoke-direct {v1, v2, v3}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 437
    .local v1, "intent":Landroid/content/Intent;
    invoke-virtual {v1, v0}, Landroid/content/Intent;->putExtras(Landroid/os/Bundle;)Landroid/content/Intent;

    .line 441
    const-string v2, "function_code"

    const/16 v3, 0x401

    invoke-virtual {v1, v2, v3}, Landroid/content/Intent;->putExtra(Ljava/lang/String;I)Landroid/content/Intent;

    .line 444
    const-string v2, "login_bg_transparent"

    invoke-virtual {v1, v2, v5}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Z)Landroid/content/Intent;

    .line 446
    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    new-instance v3, Lcom/syyx/sdkproxy/ThirdPartyAPI$7;

    invoke-direct {v3}, Lcom/syyx/sdkproxy/ThirdPartyAPI$7;-><init>()V

    invoke-static {v2, v1, v3}, Lcom/qihoo/gamecenter/sdk/matrix/Matrix;->invokeActivity(Landroid/content/Context;Landroid/content/Intent;Lcom/qihoo/gamecenter/sdk/common/IDispatcherCallback;)V

    .line 498
    return-void
.end method

.method private static refreshBalance()V
    .locals 2

    .prologue
    .line 503
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_ui_instance:Landroid/app/Activity;

    new-instance v1, Lcom/syyx/sdkproxy/ThirdPartyAPI$8;

    invoke-direct {v1}, Lcom/syyx/sdkproxy/ThirdPartyAPI$8;-><init>()V

    invoke-virtual {v0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 509
    return-void
.end method

.method public static setTPValue(Ljava/lang/String;Ljava/lang/String;)V
    .locals 3
    .param p0, "key"    # Ljava/lang/String;
    .param p1, "value"    # Ljava/lang/String;

    .prologue
    .line 83
    const-string v0, "xiyouji"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "java setTPValue, k=["

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "], v=["

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "]"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 84
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    invoke-interface {v0, p0, p1}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 85
    return-void
.end method

.method public static showMMap()V
    .locals 5

    .prologue
    .line 72
    const-string v2, "xiyouji"

    const-string v3, "call showMMap"

    invoke-static {v2, v3}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 73
    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;

    invoke-interface {v2}, Ljava/util/Map;->entrySet()Ljava/util/Set;

    move-result-object v2

    invoke-interface {v2}, Ljava/util/Set;->iterator()Ljava/util/Iterator;

    move-result-object v0

    .line 74
    .local v0, "iterator":Ljava/util/Iterator;
    :goto_0
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    move-result v2

    if-nez v2, :cond_0

    .line 78
    return-void

    .line 75
    :cond_0
    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Ljava/util/Map$Entry;

    .line 76
    .local v1, "mapEntry":Ljava/util/Map$Entry;
    const-string v2, "xiyouji"

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "k="

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-interface {v1}, Ljava/util/Map$Entry;->getKey()Ljava/lang/Object;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, ", v="

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-interface {v1}, Ljava/util/Map$Entry;->getValue()Ljava/lang/Object;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    goto :goto_0
.end method

.method public static switchAccount()V
    .locals 2

    .prologue
    .line 290
    const-string v0, "xiyouji"

    const-string v1, "nima 360 switchAccount---------------"

    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 292
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_ui_instance:Landroid/app/Activity;

    .line 293
    new-instance v1, Lcom/syyx/sdkproxy/ThirdPartyAPI$4;

    invoke-direct {v1}, Lcom/syyx/sdkproxy/ThirdPartyAPI$4;-><init>()V

    .line 292
    invoke-virtual {v0, v1}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 306
    return-void
.end method


# virtual methods
.method protected doAntiAddictionQuery(Ljava/lang/String;Ljava/lang/String;)V
    .locals 4
    .param p1, "qihooUserId"    # Ljava/lang/String;
    .param p2, "accessToken"    # Ljava/lang/String;

    .prologue
    .line 662
    new-instance v0, Landroid/os/Bundle;

    invoke-direct {v0}, Landroid/os/Bundle;-><init>()V

    .line 664
    .local v0, "bundle":Landroid/os/Bundle;
    const-string v2, "access_token"

    invoke-virtual {v0, v2, p2}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 666
    const-string v2, "qihoo_user_id"

    invoke-virtual {v0, v2, p1}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 669
    const-string v2, "function_code"

    const/16 v3, 0x804

    invoke-virtual {v0, v2, v3}, Landroid/os/Bundle;->putInt(Ljava/lang/String;I)V

    .line 670
    new-instance v1, Landroid/content/Intent;

    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    const-class v3, Lcom/qihoo/gamecenter/sdk/activity/ContainerActivity;

    invoke-direct {v1, v2, v3}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 671
    .local v1, "intent":Landroid/content/Intent;
    invoke-virtual {v1, v0}, Landroid/content/Intent;->putExtras(Landroid/os/Bundle;)Landroid/content/Intent;

    .line 673
    sget-object v2, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    new-instance v3, Lcom/syyx/sdkproxy/ThirdPartyAPI$9;

    invoke-direct {v3, p0}, Lcom/syyx/sdkproxy/ThirdPartyAPI$9;-><init>(Lcom/syyx/sdkproxy/ThirdPartyAPI;)V

    invoke-static {v2, v1, v3}, Lcom/qihoo/gamecenter/sdk/matrix/Matrix;->execute(Landroid/content/Context;Landroid/content/Intent;Lcom/qihoo/gamecenter/sdk/common/IDispatcherCallback;)V

    .line 680
    return-void
.end method

.method protected doSdkRealNameRegister(Lcom/syyx/sdkproxy/QihooUserInfo;Z)V
    .locals 3
    .param p1, "usrinfo"    # Lcom/syyx/sdkproxy/QihooUserInfo;
    .param p2, "isLandScape"    # Z

    .prologue
    .line 736
    invoke-direct {p0, p1}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->checkLoginInfo(Lcom/syyx/sdkproxy/QihooUserInfo;)Z

    move-result v1

    if-nez v1, :cond_0

    .line 747
    :goto_0
    return-void

    .line 739
    :cond_0
    if-eqz p1, :cond_1

    invoke-virtual {p1}, Lcom/syyx/sdkproxy/QihooUserInfo;->getId()Ljava/lang/String;

    move-result-object v1

    :goto_1
    invoke-direct {p0, p2, v1}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->getRealNameRegisterIntent(ZLjava/lang/String;)Landroid/content/Intent;

    move-result-object v0

    .line 741
    .local v0, "intent":Landroid/content/Intent;
    sget-object v1, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    new-instance v2, Lcom/syyx/sdkproxy/ThirdPartyAPI$11;

    invoke-direct {v2, p0}, Lcom/syyx/sdkproxy/ThirdPartyAPI$11;-><init>(Lcom/syyx/sdkproxy/ThirdPartyAPI;)V

    invoke-static {v1, v0, v2}, Lcom/qihoo/gamecenter/sdk/matrix/Matrix;->invokeActivity(Landroid/content/Context;Landroid/content/Intent;Lcom/qihoo/gamecenter/sdk/common/IDispatcherCallback;)V

    goto :goto_0

    .line 739
    .end local v0    # "intent":Landroid/content/Intent;
    :cond_1
    const/4 v1, 0x0

    goto :goto_1
.end method

.method protected doSdkUploadScore(Lcom/syyx/sdkproxy/QihooUserInfo;)V
    .locals 3
    .param p1, "usrInfo"    # Lcom/syyx/sdkproxy/QihooUserInfo;

    .prologue
    .line 686
    invoke-direct {p0, p1}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->checkLoginInfo(Lcom/syyx/sdkproxy/QihooUserInfo;)Z

    move-result v1

    if-nez v1, :cond_0

    .line 697
    :goto_0
    return-void

    .line 688
    :cond_0
    invoke-direct {p0}, Lcom/syyx/sdkproxy/ThirdPartyAPI;->getUploadScoreIntent()Landroid/content/Intent;

    move-result-object v0

    .line 689
    .local v0, "intent":Landroid/content/Intent;
    sget-object v1, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sContext:Landroid/content/Context;

    new-instance v2, Lcom/syyx/sdkproxy/ThirdPartyAPI$10;

    invoke-direct {v2, p0}, Lcom/syyx/sdkproxy/ThirdPartyAPI$10;-><init>(Lcom/syyx/sdkproxy/ThirdPartyAPI;)V

    invoke-static {v1, v0, v2}, Lcom/qihoo/gamecenter/sdk/matrix/Matrix;->execute(Landroid/content/Context;Landroid/content/Intent;Lcom/qihoo/gamecenter/sdk/common/IDispatcherCallback;)V

    goto :goto_0
.end method
