from django.contrib import admin
from django.http.request import HttpRequest
from base.models import Chercheur,Laboratoire,Article,Stock,Benefit,Stagiare,Appareil,Analyse,Rendez_vou,Experience,Echantillon,Slider
from django.db.models import Q
from django.utils.safestring import mark_safe
class SliderAdmin(admin.ModelAdmin):
    fields=("image","titre","contenue","lien","photo")
    list_display=("image","titre")
    readonly_fields=("image",)
# Register your models here.
class AppareilAdmin(admin.ModelAdmin):
     def save_model(self, request, obj, form, change):
        # Set the current user as the user for the invoice
        labo=Laboratoire.objects.get(matriculeChr__userChr=request.user)
        obj.codeLabo = labo
        super().save_model(request, obj, form, change)
     def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return  super().has_delete_permission(request, obj) 
        if obj is not None and obj.codeLabo.matriculeChr.userChr.id != request.user.id:
            return False
        return super().has_delete_permission(request, obj)
     def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return  super().has_change_permission(request, obj) 
        if obj is not None and obj.codeLabo.matriculeChr.userChr.id != request.user.id:
            return False
        return super().has_change_permission(request, obj)
     fields=("idApr", "numSerieApr", "designationApr", "frequenceMaintenanceApr", "dateAchatApr", "marqueApr", "FournisseurApr")
     list_filter=("marqueApr", "FournisseurApr")
     list_display=("idApr", "numSerieApr", "designationApr","codeLabo")
     search_fields=("idApr", "numSerieApr", "designationApr")
class ChercheurAdmin(admin.ModelAdmin):
    fields=('photo','photoChr','matriculeChr', 'nomChr', 'prenomChr', 'telChr', 'mailChr',  'specialiteChr')
    list_filter = ('specialiteChr', )
    search_fields=('matriculeChr','nomChr','prenomChr')
    list_display = ('photo','matriculeChr', 'nomChr', 'prenomChr', 'telChr', 'mailChr',  'specialiteChr')
    readonly_fields=('photo',)
class LaboratoirerAdmin(admin.ModelAdmin):
    fields= ('codeLabo', 'designationLabo', 'departementLabo', 'matriculeChr')
    list_filter = ('departementLabo',)
    search_fields=('codeLabo', 'designationLabo')
    list_display = ('codeLabo', 'designationLabo', 'departementLabo', 'matriculeChr')
class StockAdminInline(admin.TabularInline):
    model = Stock
    readonly_fields =("codeStock", "entreStock", "qtStock", "dateStock", "codeArt")
    can_delete = False
class BenefitAdminInline(admin.TabularInline):
    model = Benefit
class EchantillonAdminInline(admin.TabularInline):
    model = Echantillon
    #fields=("codeEch", "numEch", "conditionOperatoireEch", "resultatEch", "codeExp")
class ArticleAdmin(admin.ModelAdmin):
    fields=('codeArt', 'designationArt', 'typeArt', 'fournisseurArt', 'stockMinArt', 'stockMaxArt', 'moyLivraisonArt','natureArt', 'marqueArt')
    list_filter = ('typeArt', 'fournisseurArt', 'natureArt', 'marqueArt')
    search_fields=('codeArt', 'designationArt')
    list_display = ('codeArt', 'designationArt', 'typeArt', 'stock','natureArt', 'marqueArt')
    readonly_fields = ('stock',)
    inlines=[StockAdminInline,]
class StagiareAdmin(admin.ModelAdmin):
    fields= ("codeStg", "themeStg", "debutStg","finStg", "encadreur","matriculeChr1","matriculeChr2" , "codeLabo")
    list_filter =("codeLabo",) 
    search_fields=("codeStg", "themeStg","encadreur","matriculeChr1","matriculeChr2" )
    list_display =("codeStg", "matriculeChr1","matriculeChr2" , "codeLabo") 
    readonly_fields =("codeStg",) 
    inlines=(BenefitAdminInline,)
class AnalyseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Set the current user as the user for the invoice
        chercheur=Chercheur.objects.get(userChr=request.user)
        obj.matriculeChr = chercheur
        super().save_model(request, obj, form, change)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers can see all invoices
        chercheur=Chercheur.objects.get(userChr=request.user)
        if request.user.groups.filter(name='Chef de laboratoire').exists():
            chercheur=Chercheur.objects.get(userChr=request.user)
            return qs.filter(Q(idApr__codeLabo__matriculeChr=chercheur) | Q(matriculeChr=chercheur.pk))
        return qs.filter(matriculeChr=chercheur.pk)
    def download_pdf(self, obj):
        return mark_safe(f'<a target="_blank" href="/generate_pdf/analyse/{obj.codeAnly}/"><i class="fa fa-file-pdf"></i></a>')
    download_pdf.short_description = 'Download PDF'
    fields=("codeAnly","matriculeChr", "dateAnly", "cardeAnly", "natureAnly", "typeAnly", "echantillonAnly", "idApr")
    list_filter=("natureAnly", "typeAnly","idApr", "matriculeChr")
    search_fields=("codeAnly", "cardeAnly")
    list_display=("codeAnly", "dateAnly", "cardeAnly", "matriculeChr","download_pdf")
    readonly_fields=("codeAnly","matriculeChr")
class AppareilNameFilter(admin.SimpleListFilter):
    title = 'Appareil Name'
    parameter_name = 'appareil_name'
    def lookups(self, request, model_admin):
        if request.user.is_superuser:
             appareil_names = Appareil.objects.all().values_list('idApr', flat=True).distinct()
        else:
            chercheur=Chercheur.objects.get(userChr=request.user)
            appareil_names = Appareil.objects.filter(codeLabo__matriculeChr=chercheur).values_list('idApr', flat=True).distinct()
        return [(name, name) for name in appareil_names]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(codeanly__idApr=self.value())
        return queryset
class Rendez_vousAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers can see all invoices
        chercheur=Chercheur.objects.get(userChr=request.user)
        if request.user.groups.filter(name='Chef de laboratoire').exists():
            chercheur=Chercheur.objects.get(userChr=request.user)
            return qs.filter(Q(codeanly__idApr__codeLabo__matriculeChr=chercheur) | Q(codeanly__matriculeChr=chercheur.pk))
        return qs.filter(codeanly__matriculeChr=chercheur.pk)
    fields=("codeRndv", "dateRndv", "depuisRndv", "jusquaRndv", "obsRndv", "codeanly")
    list_filter=("dateRndv",AppareilNameFilter)
    search_fields=("codeRndv","obsRndv")
    list_display=("codeRndv","appareil","dateRndv", "depuisRndv", "jusquaRndv", "codeanly")
    ordering = ('-dateRndv',"-depuisRndv","jusquaRndv")
    readonly_fields=("codeRndv","appareil")
class ExperienceAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers can see all Experiences
        chercheur=Chercheur.objects.get(userChr=request.user)
        if request.user.groups.filter(name='Chef de laboratoire').exists():
            return qs.filter(Q(codeChr__matriculeChrs_1__codeLabo__matriculeChr=chercheur)| Q(codeChr__matriculeChrs_2__codeLabo__matriculeChr=chercheur) | Q(codeChr=chercheur.pk))
        return qs.filter(codeChr=chercheur.pk)
    fields=("codeExp", "dateExp", "titreExp", "methodeExp", "conclusionExp", "idApr","codeChr")
    list_filter =("dateExp","methodeExp","idApr","codeChr")
    search_fields=("codeExp", "titreExp","conclusionExp")
    list_display =("codeExp", "dateExp", "titreExp","codeChr")
    readonly_fields =("codeExp",)
    inlines=(EchantillonAdminInline,)
admin.site.register(Slider,SliderAdmin)
admin.site.register(Laboratoire,LaboratoirerAdmin)
admin.site.register(Chercheur,ChercheurAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Stagiare,StagiareAdmin)
admin.site.register(Appareil,AppareilAdmin)
admin.site.register(Analyse,AnalyseAdmin)
admin.site.register(Rendez_vou,Rendez_vousAdmin)
admin.site.register(Experience,ExperienceAdmin)