from django.db import models
from django.utils.safestring import mark_safe
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_delete
from django.contrib.auth.models import Group
import datetime


class Slider(models.Model):
    titre=models.CharField(max_length=256)
    photo=models.ImageField(upload_to="sliders/",null=True)
    contenue=models.TextField(max_length=5000)
    lien=models.URLField()
    def image(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.photo.url))
    image.short_description='image'
    image.allow_tags=True
# Create your models here.
class Chercheur(models.Model):
    matriculeChr=models.CharField(verbose_name="Matricule",primary_key=True,max_length=13)
    nomChr=models.CharField(verbose_name="Nom",max_length=50,null=False)
    prenomChr=models.CharField(verbose_name="Prenom",max_length=50,null=False)
    mailChr=models.EmailField(verbose_name="Email")
    telChr=models.BigIntegerField(verbose_name="Telephone ",null=True, blank=True, unique=True,)
    photoChr=models.ImageField(verbose_name="photo source",upload_to="chercheur")
    specialiteChr=models.CharField(verbose_name="Specialite",max_length=100)
    userChr=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    def photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.photoChr.url))
    photo.short_description='Photo'
    photo.allow_tags=True
    def __str__(self) -> str:
        return self.matriculeChr+"|"+self.nomChr+"|"+self.prenomChr
    def nom_prenom(self):
        return self.nomChr+" "+self.prenomChr
class Laboratoire(models.Model):
    class Departement(models.TextChoices):
        chimie_macromoleculaire="chimie macromoléculaire"
        chimie_et_physique_des_materiaux_inorganiques="chimie et physique des matériaux inorganiques"
        chimie_organique="chimie organique"
        chimie_physique_et_throrique="chimie physique et théorique"
    codeLabo=models.IntegerField(verbose_name="Numero",primary_key=True)
    designationLabo=models.CharField(verbose_name="Nom",max_length=50,blank=False,null=False)
    departementLabo=models.CharField(verbose_name="Département de",max_length=50,choices=Departement.choices)
    matriculeChr=models.ForeignKey(Chercheur,on_delete=models.SET_NULL,verbose_name="Chef de Laboratoire",null=True)
    def __str__(self):
        return str(self.codeLabo)+"|"+self.designationLabo
class Article (models.Model):
    codeArt=models.CharField(verbose_name="Code",max_length=10,primary_key=True)
    designationArt=models.CharField(verbose_name="Designation",max_length=150)
    typeArt=models.BooleanField(verbose_name="is Produit Chimique",default=True)
    fournisseurArt=models.CharField(verbose_name="Fournisseur",max_length=100)
    stockMinArt=models.FloatField(verbose_name="Stock Minimum")
    stockMaxArt=models.FloatField(verbose_name="Stock Minimum")
    moyLivraisonArt=models.IntegerField(verbose_name="moyen de Livraison par jour")
    natureArt=models.CharField(verbose_name="Nature",max_length=50)
    marqueArt=models.CharField(verbose_name="Marque",max_length=50)
    def stock(self):
        try:
            sum=Stock.objects.filter(entreStock=True).aggregate(total=Sum('qtStock'))['total']-Stock.objects.filter(entreStock=False).aggregate(total=Sum('qtStock'))['total']
        except:
            return 0
        else:
            return sum 

    def __str__(self):
        return str(self.codeArt)+"|"+self.designationArt
class Stock(models.Model):
    codeStock=models.AutoField(verbose_name="Numero",primary_key=True)
    entreStock=models.BooleanField(verbose_name="is Entre")
    qtStock=models.FloatField(verbose_name="Quantite")
    dateStock=models.DateField(verbose_name="Date",default=datetime.date.today)
    codeArt=models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name="Article")

class Stagiare(models.Model):
    #(codeStg, themeStg, debutStg, finStg, #encadreur,#matriculeChr1,#matriculeChr2 , #codeLabo)
    codeStg=models.AutoField(verbose_name="Numero",primary_key=True)
    themeStg=models.CharField(verbose_name="Theme",max_length=150)
    debutStg=models.DateField(verbose_name="Debut de Stage")
    finStg=models.DateField(verbose_name="Fin de Stage")
    encadreur=models.ForeignKey(Chercheur,on_delete=models.SET_NULL,related_name='encadreurs',null=True,verbose_name="Encadreur")
    matriculeChr1=models.ForeignKey(Chercheur,on_delete=models.SET_NULL,related_name='matriculeChrs_1',null=True,verbose_name="Stagiare")
    matriculeChr2=models.ForeignKey(Chercheur,on_delete=models.SET_NULL,related_name='matriculeChrs_2',null=True,verbose_name="Stagiare")
    codeLabo=models.ForeignKey(Laboratoire,on_delete=models.SET_NULL,null=True,verbose_name="Laboratoire")
class Benefit(models.Model): 
    #(#codeArt,# matriculeChr, qtDB, qtRB)
    codeArt=models.ForeignKey(Article,on_delete=models.SET_NULL,null=True)
    codeStg=models.ForeignKey(Stagiare,on_delete=models.CASCADE)
    qtDB=models.FloatField(verbose_name="Quantite Demande")
    qtRB=models.FloatField(verbose_name="Quantite Receptionne")
class Appareil(models.Model):
    idApr=models.CharField(verbose_name="Code d'Appareil",max_length=30,primary_key=True)
    numSerieApr=models.CharField(verbose_name="Numero d'Serie",max_length=20)
    designationApr=models.CharField(verbose_name="Nom d'Appareil",max_length=100)
    frequenceMaintenanceApr=models.IntegerField(verbose_name="Frequence de Maintenance Par jour")
    dateAchatApr=models.DateField(verbose_name="Date d'Achat")
    marqueApr=models.CharField(verbose_name="Marque",max_length=50)
    FournisseurApr=models.CharField(verbose_name="Fournisseur",max_length=100)
    codeLabo=models.ForeignKey(Laboratoire,on_delete=models.SET_NULL,verbose_name="Laboratoire",null=True)
    def __str__(self):
        return self.idApr+"|"+self.designationApr
    def abrv(self):
        return self.idApr.replace(self.numSerieApr, '')
class Analyse(models.Model):
    #(codeAnly, dateAnly, cardeAnly, natureAnly, typeAnly, echantillonAnly, idApr, matriculeChr)
    codeAnly=models.AutoField(verbose_name="Numero",primary_key=True)
    dateAnly=models.DateField(verbose_name="Date de Demande",default=datetime.date.today)
    cardeAnly=models.CharField(verbose_name="Card",max_length=100)
    natureAnly=models.CharField(verbose_name="Nature",max_length=50)
    typeAnly=models.CharField(verbose_name="Type",max_length=50)
    echantillonAnly=models.IntegerField(verbose_name="Nombre d'chantillon")
    idApr=models.ForeignKey(Appareil,on_delete=models.SET_NULL,verbose_name="Appareil",null=True)
    matriculeChr=models.ForeignKey(Chercheur,on_delete=models.SET_NULL,verbose_name="Chercheur",null=True)
    def __str__(self):
        return str(self.codeAnly)
class Rendez_vou(models.Model):
    #("codeRndv", "dateRndv", "depuisRndv", "jusquaRndv", "obsRndv", "codeanly")
    codeRndv=models.AutoField(verbose_name="Code Rendez-vous",primary_key=True)
    codeanly=models.OneToOneField(Analyse,verbose_name="Numero de demande",on_delete=models.CASCADE)
    dateRndv=models.DateField(verbose_name="Date",default=datetime.date.today)
    depuisRndv=models.TimeField(verbose_name="de puis")
    jusquaRndv=models.TimeField(verbose_name="jusqu'a")
    obsRndv=models.TextField(verbose_name="Observation",max_length=2000)
    def appareil(self):
        return self.codeanly.idApr.idApr
class Experience(models.Model): 
    #(codeExp, dateExp, titreExp, methodeExp, conclusionExp, idApr,codeStg)
    codeExp=models.AutoField(verbose_name="Code Experience",primary_key=True)
    codeChr=models.ForeignKey(Chercheur,on_delete=models.SET_NULL,null=True, verbose_name="Chercheur")
    idApr=models.ForeignKey(Appareil,on_delete=models.SET_NULL,null=True, verbose_name="Appareil")
    dateExp=models.DateField(verbose_name="Date",default=datetime.date.today)
    titreExp=models.CharField(verbose_name="Titre",max_length=150)
    methodeExp=models.TextField(verbose_name="MethodeExp",max_length=5000)
    conclusionExp=models.TextField(verbose_name="Conclusion",max_length=5000)
class Echantillon(models.Model):
    #(codeEch, numEch, conditionOperatoireEch, resultatEch, codeExp)
    codeEch=models.AutoField(verbose_name="code echantillon",primary_key=True)
    numEch=models.IntegerField(verbose_name="N°")
    conditionOperatoireEch=models.TextField(verbose_name="Condition Operatoire",max_length=1000)
    resultatEch=models.TextField(verbose_name="Resultat",max_length=1000)
    codeExp=models.ForeignKey(Experience,on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['codeEch', 'numEch'], name='unique_codeech_numech_combination'
            )
        ]
def create_user_profile(sender, instance, created, **kwargs):
        if created:
            user = User.objects.create_user(
            username=instance.nomChr+"_"+instance.prenomChr,
            email=instance.mailChr,
            password=instance.matriculeChr,
            is_staff=True
            )
            instance.userChr = user
            instance.save()
            my_group = Group.objects.get(name='chercheur') 
            my_group.user_set.add(user)
def delete_user_profile(sender, instance, **kwargs):
    user = Chercheur.objects.filter(userChr=instance.id)  
    user.delete()

pre_delete.connect(delete_user_profile, sender=User)
post_save.connect(create_user_profile, sender=Chercheur)