# Pehle Paisa Browser - Charan 1

Kya hai: WebView par bana simple Android browser. Address bar, tabs, home par common sites, aur built-in list se trackers block (upar counter).

## Kaise chalayein
1. Android Studio (Koala ya naya) kholo. File > Open > is folder ko chuno.
2. Gradle sync hone do (pehli baar internet chahiye).
3. Phone mein Developer options > USB debugging on karo, phone jodo, Run dabao.

## Agar sync mein dikkat aaye
File > New > New Project > Empty Views Activity (Kotlin), package com.pehlepaisa.browser. Fir yahan se ye files copy karo:
- MainActivity.kt aur TrackerBlocker.kt
- res/layout/activity_main.xml, res/values/themes.xml, res/values/strings.xml
- AndroidManifest.xml (INTERNET permission zaroor)
- app/build.gradle.kts mein appcompat dependency

## Charan 2 mein
Badi tracker list (EasyPrivacy), per-site ijazat screen, wallet.
