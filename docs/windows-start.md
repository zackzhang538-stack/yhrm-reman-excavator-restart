# Windows 开工说明 · 永鸿挖掘机再制造教学项目

## 要交的作品

为永鸿做一部有独立创意的再制造品牌作品。它面向海外采购商、设备经销商和出口贸易商。观众应能看懂旧机经过了哪些处理、永鸿怎样判断一件东西值得修或需要换，还应愿意停下来看，享受机械拆合的力量、精度和节奏，看完记得一个属于永鸿的瞬间。创作者可以提出更有价值的观看体验，并用样段说明自己的选择。

复用已核过的模型、零件身份和文件证据。保留真实工序及可核对的机械动作，区分实机工单和教学示意。叙事从哪一刻开始、用谁的视角、声音何时先于画面、怎样展开或重组、一个动作持续多久，由 Windows 创作团队独立决定。

上次旧六缸总览最大展开时，主体约占画宽五分之一，客户难以辨认内部件。另一次量完曲轴轴颈就切到更换下瓦，画面缺少换件依据。这两条教训用于核查观众看到了什么、能据此得出什么结论。新片的主角和开场由新团队选择。

## 第一次在 Windows 上开机

**账号。** Blender 桌面软件和下述本机控制桥都可以直接使用。Codex 如已登录就沿用现有会话，首次使用可选「使用 ChatGPT 登录」。这是私有 GitHub 仓库，使用有访问权的 GitHub 账号在浏览器授权。密码、验证码、恢复码由本人在官方界面输入。优先使用 Windows 原生桌面和 PowerShell，以便 Codex 与桌面 Blender 访问相同目录。[Codex 登录](https://developers.openai.com/codex/auth/) · [GitHub CLI 登录](https://cli.github.com/manual/gh_auth_login)

1. 在固定本地目录工作，例如用户目录下的 `YHRM`，仓库、下载原件和工作副本各用一个子目录。安装并启动一次官方 **Blender 5.3.0**。这是 Mac 重开过整机的版本。通常 Intel/AMD 电脑选 Windows x64，ARM 电脑选 ARM64。先确认本机系统类型。[Blender 5.3 官方 Windows 安装包](https://download.blender.org/release/Blender5.3/)
2. 用浏览器登录 GitHub 后可直接查看仓库和 Release。采用命令行时先检查 Git、GitHub CLI 和 uv，缺哪项再装哪项，然后重新打开 PowerShell。以下示例用于首次在新目录接手；目录里已有文件时先检查现有副本。[GitHub CLI](https://cli.github.com/) · [uv 在 Windows 上的安装](https://docs.astral.sh/uv/getting-started/installation/)

   ```powershell
   # 按缺少的工具分别执行
   winget install --id Git.Git -e
   winget install --id GitHub.cli -e
   winget install --id astral-sh.uv -e
   ```

   ```powershell
   gh auth status
   # 尚未以有权账号登录时执行
   gh auth login --hostname github.com --web --git-protocol https
   gh auth setup-git
   $projectRoot = Join-Path $env:USERPROFILE 'YHRM'
   New-Item -ItemType Directory -Force -Path $projectRoot | Out-Null
   Set-Location $projectRoot
   gh repo clone zackzhang538-stack/yhrm-reman-excavator-restart repo
   gh release download restart-v1.0.0 -R zackzhang538-stack/yhrm-reman-excavator-restart -p '*.blend' -p 'SHA256SUMS.txt' -D baseline
   Get-FileHash '.\baseline\YHRM-excavator-teaching-assembly-80a7.blend' -Algorithm SHA256
   ```

3. 比对整机摘要 `80a792514b4a4baaafee2d658da0ed344efbbd3a73f8a5736b18bd1194d5b7e9`。用实际安装路径下的 `blender.exe` 独立读回文件，看到 `PASS_INDEPENDENT_REOPEN` 后核对主场景 8,901 个对象、8,811 个网格、16 个场景及外部资源记录。随后复制为 `work\YHRM_work_01.blend`，在桌面 Blender 打开这份副本。仓库的七个 STEP 是与整机网格核对过的项目自建件，其证明范围见[资产与证据](资产与证据.md)。

   ```powershell
   # 在上述项目根目录执行。Blender 如安装在其他目录，替换第一行
   $blenderExe = Join-Path $env:ProgramFiles 'Blender Foundation\Blender 5.3\blender.exe'
   & $blenderExe -b --disable-autoexec '.\baseline\YHRM-excavator-teaching-assembly-80a7.blend' --python-exit-code 1 --python '.\repo\tools\inspect_blend.py'
   ```

4. 接通桌面 Blender。项目在 Mac 使用过 `ahujasid/mcp-for-blender`。Windows 建议从同一项目的 PyPI 2.2.8 发行包装起，用实际操作验收。它与 Mac 固定源码构建存在差异。先关闭 Blender，安装对应版本插件，再打开 Blender，在「编辑 → 偏好设置 → 插件」启用 MCP for Blender，在 3D 视图按 N 查看 MCP 面板和服务状态。本机监听 `127.0.0.1:9876`。如服务已自动启动，直接连接。[发行包与安装指引](https://pypi.org/project/mcp-for-blender/2.2.8/) · [项目说明](https://github.com/ahujasid/mcp-for-blender/blob/578360f8007ce6818b1a3c8b2cfe731f9283ed45/README.md)

   ```powershell
   uvx --from mcp-for-blender==2.2.8 mcp-for-blender install-addon
   ```

   在 Codex 的 MCP 设置添加一个本机 STDIO 服务，名称 `blender`。命令填 `(Get-Command uvx.exe).Source` **输出的真实路径**，参数逐项填 `--from`、`mcp-for-blender==2.2.8`、`mcp-for-blender`，环境变量填 `BLENDER_HOST=127.0.0.1`、`BLENDER_PORT=9876`、`DISABLE_TELEMETRY=true`。已安装 Codex CLI 的机器也可用下列等价配置，选择一种即可。若已有同名项，先核配置。[Codex MCP 配置](https://developers.openai.com/codex/mcp/)

   ```powershell
   $uvxExe = (Get-Command uvx.exe).Source
   codex mcp add blender --env BLENDER_HOST=127.0.0.1 --env BLENDER_PORT=9876 --env DISABLE_TELEMETRY=true -- $uvxExe --from mcp-for-blender==2.2.8 mcp-for-blender
   ```

5. 重新载入 Codex 的连接。在已打开工作副本的 Blender 桌面会话，通过 MCP 读出 `bpy.data.filepath`、活动场景名和当前帧，取一张视口截图，再让 Codex 改变视角或选中一件模型零件，让使用者能在屏幕上看到对应变化。将工作副本路径和截图随首份回报发回。这是 Windows 本机首次验收，Mac 的成功记录供比对。

## 怎样从参考中形成自己的意见

各人先独立写出最想让观众感到什么、能从永鸿的哪个真实细节获得这种感受，再看参考和旧片。由创作者决定研究哪部作品。以下是题主发来的原始线索和工程案例，可据此核查来源。

| 学习方向 | 参考 |
|---|---|
| 拆解时如何建立空间感，镜头如何揭示一道工序 | [小淇 · 挖掘机拆解](https://v.douyin.com/yLV-ZeDsS9I/) · [EFFE · 挖掘机液压系统项目](https://3danimation.in/projects/3d-product-animation-for-excavator/) |
| 白模导演预演与原生动作控制 | 太阳鸽鸽的[Blender 做导演](https://v.douyin.com/vI0Owrf0_As/)和[导演 Skill](https://v.douyin.com/nRjwCLzRCxk/) · [作者的预演介绍](https://www.youtube.com/watch?v=Feb1FAFjXpc) |
| Codex 与 Blender 的实际操作、模型和动作能否重放 | [子鱼在此](https://v.douyin.com/_qQqLxJ_1PQ/) · [椎希](https://v.douyin.com/z5BhhBv4PmM/) · [极简 AI](https://v.douyin.com/Wym0zuX_Lus/) |
| 如何用实物痕迹与检查记录建立诊断依据 | [MAHLE 轴瓦失效图解](https://www.mahle-aftermarket.com/na/en/support/failure-analysis/) · [Motorservice 技师演示](https://www.youtube.com/watch?v=tX9op7dYhmI) |

也可跨出工程机械行业找灵感，例如纪录片怎样让一个判断产生悬念，声音设计怎样让人感到重量。对真正看过的片段，说清是哪一个时刻、为什么有效、搬到永鸿现场要靠什么成立。上轮有几条抖音只核到作者、标题或简介；逐镜判断须以可播放的片源为据。

## 第一次创意交付

在任何一件零件进入精修前，先提出两个出发点真正不同的构思，各用两三句话回答「跟着谁或什么看」「什么变化会让人继续看」「哪个属于永鸿的细节能撑得住这个想法」。如果换了音乐、机位或灯光，两个构思仍在讲同一件事，就继续想。导演选出自己最看好的一条，把时间花在它最难、最值得看的那段。若懂行的人没有理由相信这个动作，或需要虚构永鸿的能力才能成立，先换表达。

第一次给使用者看一段正常速度可播的原生动作预演，附一份可重开的 Blender 工作副本和一张能体现最终美感的代表画面。样段选在哪里、用哪个总成和持续多久，以叙事需要为准。第三缸的自建 CAD 核对较充分，可作工具或几何测试素材。追求拆散与归位的机械美感，同时让观众认得出同一个部件、看得见动作的因果。声音可以在构思阶段参与设计。

看完先问观众「你最想再看哪一秒？你记住永鸿的哪件事？片中哪一个细节让你相信它？」再请懂机械的人指出失真或证据不足的画面。涉及拆检的段落另检查静音后能否辨认动作和检查面。若观众只能复述流程，品牌创意还需要迭代。导演依据反馈修最影响观感的一处，再扩展全片。

## 整机与工艺的验收

工程核查可以与创意预演并行。用四视图和开盖图查机壳与配重、管线防护、斗杆铰接、履带端部和登车踏步。涉及实际维修时核实支承、工具和连续拆装空间。不同角色各交独立副本，主控核对版本和接口再合入。

完整作品涵盖旧机评估、清洗拆解、逐件检测、修复或换新及复验、适用件表面处理、部件验收、整机组装、性能检测、交付与售后。查实工序先后和判断依据。影片可以倒叙、交叉讲述或选用其他形式，观众能还原实际因果即可。工程检查细目见[模型重启流程](重启流程.md)，实际适用数据见[资产与证据](资产与证据.md)。
