# macOS: KosmicKrisp как основной путь

Решение от 2026-10-21: Apple Silicon/macOS 26+ → Vulkan Loader → KosmicKrisp → Metal 4. В каркасе драйвер и loader не подключены.

## Проверенные исходные данные

- [Mesa: KosmicKrisp](https://docs.mesa3d.org/drivers/kosmickrisp.html): Vulkan-реализация поверх Metal 4 для Apple Silicon, требующая macOS 26+.
- [Khronos, 1 октября 2026](https://www.khronos.org/news/archives/kosmickrisp-achieves-vulkan-1.4-conformance-on-apple-silicon): заявлена Vulkan 1.4 conformance.
- [LunarG, 15 октября 2026](https://www.lunarg.com/the-state-of-vulkan-on-apple-oct-2026/): KosmicKrisp — предпочтительный путь для современных Apple Silicon desktop; MoltenVK сохраняет применение для старых ОС и других конфигураций.

Дата проверки источников: 2026-10-21. Не переносим прежнее обязательное требование MoltenVK portability subset на KosmicKrisp. Conformance не подтверждает совместимость с нашей будущей нагрузкой: она проверяется отдельно.

## Профили

| Конфигурация | Политика Foundation |
|---|---|
| Apple Silicon, macOS 26+ | Основной обязательный профиль, KosmicKrisp |
| Apple Silicon, более ранняя macOS | Legacy-кандидат; пока не поддерживается и не обещается |
| Intel Mac | Legacy-кандидат; KosmicKrisp не является решением |
| iOS, tvOS и другие Apple-платформы | За пределами первой версии |

MoltenVK не закладываем в архитектуру как обязательный runtime. Возможность legacy-профиля рассматривается отдельно после реализации основного пути. Это выбор проекта; не утверждение, что MoltenVK полностью прекратил существование или поддержку.

## Выбор драйвера и поставка

Бэкенд остаётся Vulkan-бэкендом. Выбор ICD и проверка возможностей относятся к bootstrap/platform policy. Диагностика записывает фактические driver ID, версию, устройство и доступные features, без предположения «на macOS всегда MoltenVK».

Требуется зафиксированная протестированная поставка loader/ICD без установки SDK пользователем. Для интеграции с существующей Steam-игрой нужно отдельно проверить layout sidecar/app bundle, загрузку native-библиотек и требования подписи. Изменение системных библиотек, отключение защит macOS и глобальная настройка драйвера не являются планом установки.

## Ранние проверки

В первой лаборатории обязательны запуск без системного SDK, native-library discovery, resize, Retina/fractional scaling, fullscreen, сон/возврат, сворачивание, depth/stencil, alpha, texture arrays, offscreen images, compute, upload и readback. Записываются версии ОС, GPU, драйвера и инструментария. Не заявляем поддержку по одному треугольнику.

Ограничения features и лимитов доступны расширениям через capabilities. Продвинутые возможности не становятся частью базового профиля без проверки на минимальной поддерживаемой машине.
