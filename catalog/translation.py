from modeltranslation.translator import register, TranslationOptions
from .models import (
    Category,
    Product,
    Feature,
    Benefit,
    Document,
    Video,
    Digits,
    Color,
    Gallery,
    Manufacturer,
)


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = (
        'title',
        'meta_description',
        'meta_keywords',
        'description',
        'description_aux',
    )


@register(Product)
class ProductTranslation(TranslationOptions):
    fields = (
        'title',
        'meta_description',
        'meta_keywords',
        'description',
        'title_color',
        'title_use',
        'title_features',
        'title_benefit',
        'title_gallery',
        'title_documents',
        'title_digits',
        'title_video',
        'title_country',
        'use',
    )


@register(Feature)
class FeatureTranslation(TranslationOptions):
    fields = (
        'title',
        'value',
    )


@register(Benefit)
class BenefitTranslation(TranslationOptions):
    fields = (
        'title',
        'subtitle',
        'text',
    )


@register(Document)
class DocumentTranslation(TranslationOptions):
    fields = (
        'title',
    )


@register(Video)
class VideoTranslation(TranslationOptions):
    fields = (
        'title',
    )


@register(Digits)
class DigitsTranslation(TranslationOptions):
    fields = (
        'title',
        'subtitle',
        'text',
    )


@register(Color)
class ColorTranslation(TranslationOptions):
    fields = (
        'alt',
    )


@register(Gallery)
class GalleryTranslation(TranslationOptions):
    fields = (
        'alt',
    )


@register(Manufacturer)
class ManufacturerTranslation(TranslationOptions):
    fields = (
        'title',
        'meta_description',
        'meta_keywords',
        'description',
    )
