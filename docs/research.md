# Источники и открытые вопросы

Дата проверки: 2026-10-21. Факты источников не заменяют проверку конкретного билда и устройства. Архитектурные решения проекта находятся в ADR.

## Первичные источники

- [Mesa: KosmicKrisp](https://docs.mesa3d.org/drivers/kosmickrisp.html) — требования к современному Mac-пути.
- [Khronos: KosmicKrisp Vulkan 1.4 conformance](https://www.khronos.org/news/archives/kosmickrisp-achieves-vulkan-1.4-conformance-on-apple-silicon) — статус соответствия Vulkan.
- [LunarG: The State of Vulkan on Apple, октябрь 2026](https://www.lunarg.com/the-state-of-vulkan-on-apple-oct-2026/) — выбор драйвера и поставка Apple runtime.
- [Khronos: Synchronization](https://docs.vulkan.org/guide/latest/synchronization.html) — ответственность за синхронизацию.
- [GLFW: Vulkan guide](https://www.glfw.org/docs/latest/vulkan_guide.html) — окно, surface и loader.
- [LWJGL Vulkan bindings](https://javadoc.lwjgl.org/org/lwjgl/vulkan/package-summary.html) — доступ из Java; опубликованный latest не фиксирует версию проекта.

## Исходные сторонние исследования PZ

- [lonelyicer/zomboid-vulkan](https://github.com/lonelyicer/zomboid-vulkan) — экспериментальный предшественник. Его README обозначает неполный takeover и штатный GL passthrough. Здесь его код не скопирован, работоспособность нами не проверена.
- [PZ_Optimization: Vulkan plan](https://github.com/xD3I/PZ_Optimization/blob/master/docs/plan-vulkan-renderer.md) — чужая инвентаризация GL-путей конкретного билда. Числа и точки подключения должны быть перепроверены на выбранной версии.
- [TIS: Wayland/Vulkan discussion](https://theindiestone.com/forums/topic/29152-wayland-support-linux-and-vulkan-renderer/) — историческое обсуждение; не текущий roadmap и не контракт совместимости.

## Решить на этапе исследования

1. Какой точный билд PZ станет первым поддерживаемым и как проверять его revision?
2. Как грузить адаптер, какие методы патчить, как сохранить multiplayer integrity checks?
3. Где находятся все ванильные graphics entry points, включая вызываемые Lua-модами?
4. Какие пользовательские текстуры, модели, атласы и render targets поддерживаются штатно?
5. Какие guarantees порядка и потоков реально наблюдаются у callbacks выбранного билда?
6. Какие minimum features нужны для базового профиля Foundation на всех трёх платформах?
7. Какую связку JVM/LWJGL/native ABI позволяет выбранный билд без конфликтов?
8. Как упаковать KosmicKrisp и loader для интеграции с установленной Steam-игрой?
9. Какой набор реальных обычных модов можно законно и воспроизводимо проверять без перепубликации их содержимого?
10. Какие правила shader formats, координат, цветовых пространств и глубины подтвердит инвентаризация?

Вопросы не маскируются заглушками, которые заявляют поддержку. Реализация и окончательные сигнатуры следуют за фактами исследования.
