# Windows 开工说明 · 永鸿挖掘机再制造教学项目

## 要交的作品

让采购商和设备经销商第一次看，就能说出三件事：这台旧机为什么拆开、永鸿如何判定零件的去留、整机怎样证明可以交付。交付物是一台能在 Blender 里打开并逐层拆看的 YHRM 教学挖掘机，以及基于这台机器制作的连续工艺动画。使用永鸿自己的机身标识。模型允许采用通用结构；凡涉及某个机型、维修限值或永鸿实际能力，都要有对应依据。

上次有两个镜头足以说明问题。第一，旧六缸总览最大展开时，主体约占画宽五分之一，技术员知道里面有东西，客户却看不清。第二，量完曲轴轴颈就切到更换下瓦，两件事中间缺了诊断。重做时，每个镜头先写一句「观众看完能回答什么」，再决定需要精建哪个零件、看到哪一面、持续多久。握手连通和对象数量只说明软件和文件状态。

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

## 带着三个问题学参考

| 问题 | 去哪里看 | 在这个项目怎样用 |
|---|---|---|
| 看完一台复杂机器，怎么一直知道正在拆哪一件？ | [小淇 · 挖掘机拆解](https://v.douyin.com/yLV-ZeDsS9I/) · [EFFE · 挖掘机液压系统项目](https://3danimation.in/projects/3d-product-animation-for-excavator/) | 挑一段由整机到内部的转场，记录能播放片源的时间点、画面里的定位物和第一次看清工作面的时刻。用永鸿自己的模型同样拍一遍。 |
| 怎样先判断这个镜头值不值得渲？ | 太阳鸽鸽的[Blender 做导演](https://v.douyin.com/vI0Owrf0_As/)和[导演 Skill](https://v.douyin.com/nRjwCLzRCxk/) · [作者的白模预演介绍](https://www.youtube.com/watch?v=Feb1FAFjXpc) | 用简化材质和最终机位预演。对同一动作比较远景和近景，揭开内部后让相机停在接合面。关键面易辨再投入灯光、材质和高分辨率渲染。 |
| Codex 能不能真的控制机械对象，重复同一动作？ | [子鱼在此 · Codex 操作 Blender](https://v.douyin.com/_qQqLxJ_1PQ/) · [椎希 · 自建模自动画](https://v.douyin.com/z5BhhBv4PmM/) · [极简 AI · 六足机器人](https://v.douyin.com/Wym0zuX_Lus/) | 用一件有编号的零件做脱开、停顿和复位。保存后重开，从同一摄影视角播放，核对末帧和原装位。 |
| 哪种检查画面能解释维修判断？ | [MAHLE 发动机轴瓦失效图解](https://www.mahle-aftermarket.com/na/en/support/failure-analysis/) · [Motorservice 技师演示](https://www.youtube.com/watch?v=tX9op7dYhmI) | 区分可观察到的痕迹、可能原因、还要做的检测。参考视频中的总成类型、量值和处置条件要与所讲部件逐项对应。永鸿真实作业以工单、适用手册或工程师实证核对。 |

上轮对部分抖音链接只核到作者、标题或简介。Windows 若能播放，才填写镜头时间；遇到播放限制，就用能核实的作者案例完成对照。短视频适合学镜头，结构与修复判据回到机械资料。每项研究带回一个可演示的改动。只在遇到明确制作难点时增装工具。

## 第一轮怎么干，什么时候值得扩展

**先把整机摆对。** 用同一副本交正侧视图、俯视图、左前和右后两个斜视图，另加一张开盖图。优先看机壳与配重能否包住机舱、液压管有没有合理防护，铲斗和连杆的销轴关系能否走通，履带端部及登车踏步是否符合用途。每个可疑点标到模型对象和具体姿态。先改影响拆装或第一眼真实性的大结构，再处理螺栓、贴花和漆面。

**再用第三缸连杆大头做第一段。** 这里有已对账的连杆体、盖、上下瓦和定位套。摄像机先交代它在发动机里的位置，保留第三缸或连杆盖作为画面地标。用真实对象展开，镜头停稳，让观众看到下瓦的工作面、它与盖的配合和返回的方向。把曲轴、连杆和盖投在同一个角度里，避免剖切或转场让人误判它们的关系。若表现实际操作，先核实解除紧固、受控支承、工具接近、连续退出、复位和紧固的条件；演示空间展开时在画面上写明「结构示意」。可由下瓦检查面引入磨损教学，结论用同一件的痕迹、记录和适用判据解释。仅有名义几何时，准确讲到“检查哪里、还需什么依据”。旧版曲轴的测值和路径须在当前版本上重新核对。

**第一轮交可看的东西。** 一份可重开的工作副本，一张整机多视图和开盖图，一段建议 20–40 秒、可正常速度播放的原生白模动画，一张代表精修质量的近景，以及一页「已验证／教学示意／仍缺证据」。时长按动作可读性调整。让一位不了解项目的人静音看一遍，能指出拆了什么、检查哪里、装回哪里，再让懂机械的人核动作。看不明白，就对准那一镜改，不扩展同类镜头。精修近景要看得出铸件的粗糙表面、轴颈的机加工高光和轴瓦的工作面。用侧光显出边缘，在接触或落座时留一拍；观众看到哪两个面合上，机械感自然就出来了。

**样段定下来再铺整片。** 用永鸿实际流程逐章串起旧机评估、清洗拆解、逐件检测、修复或换新及复验、适用结构件的喷砂喷漆、部件验收入库、整机组装、性能检测、设备交付与售后。清洗让油泥随水流退去，残余锈蚀和掉漆留给下一道相应工序；同一件从检测跟到处置和复检。轴瓦、密封面等按各自工艺表现。最后明确展示已核的整机动作和有依据的试机项目。人物只在扶持、量检、清洗或尺度有助理解时出镜。声音配合工具接触与零件落座，旁白解释判定和理由。原生模型连续运动构成主画面，片长由每章需要的秒数合计，字幕和音乐最后加入。

并行可以分别研究实机结构、机械工艺和导演预演。每人用同一份冻结基线，在单独文件交结果。主控核版本、单位、对象身份、接口与动作，统一合入工作副本。每轮回报三个东西：能打开的文件、能看到的改进、仍需补的依据。
