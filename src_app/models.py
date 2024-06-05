from django.db import models
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4



class Reciter(models.Model):

    name = models.CharField(max_length=3000, verbose_name="Reciter's Name")
    gender = models.CharField(max_length=1000, choices=(('Male', 'Male'), ('Female', 'Female')),verbose_name="Gender")
    country = models.CharField(max_length=1000, verbose_name="Reciter's Country of Residence")
    img = models.ImageField(upload_to='reciters', default='', verbose_name="Reciter's Picture", blank=True)
    
    def __str__(self):

        return self.name


class Audio(models.Model):

    title = models.CharField(max_length=100000, verbose_name="Title")
    audio_file = models.FileField(upload_to='Tilawahs', verbose_name="Audio File", default='', blank=False)
    reciter = models.ForeignKey(to=Reciter, on_delete=models.CASCADE, verbose_name='Reciter')    
    kind = models.CharField(max_length=1000, choices=(('few_verses', 'few_verses'), ('surah', 'surah')), null=True)
    chapter_number = models.PositiveIntegerField(blank=True, verbose_name="Chapter Number", null=True)

    def __str__(self):

        return self.title

    def get_duration(self):
        audio_file_path = self.audio_file.path
        if audio_file_path.endswith('.mp3'):
            audio = MP3(audio_file_path)
        elif audio_file_path.endswith('.m4a'):
            audio = MP4(audio_file_path)
        else:
            return None
        return int(audio.info.length)

class Book(models.Model):

    title = models.CharField(max_length=200, verbose_name='Book Title')
    img = models.ImageField(upload_to='Books', verbose_name='Book Image', default='', blank=False)
    price = models.PositiveIntegerField(verbose_name='Price', blank=False)
    desc = models.TextField(verbose_name='Book Description', null=True)
    available = models.BooleanField(default=True, verbose_name='Book Available?')
    def __str__(self):

        return self.title 


class Order(models.Model):

    book = models.ForeignKey(to=Book, null=True, on_delete=models.DO_NOTHING, verbose_name='Ordered Books')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Ordered Product Quantity')
    total_price = models.PositiveIntegerField(default="Total Price",)
    email = models.CharField(max_length=100000, verbose_name='Customer Email', null=False, default='')
    address = models.TextField(default='', blank=False, verbose_name="Delivery Address")
    contact = models.CharField(max_length=1000, verbose_name='Contact Number')
    payment_method = models.CharField(max_length=1000, verbose_name='Payment Method', choices=(('Paypal', 'Paypal'),('Stripe','Stripe'),('Cash on delivery', 'Cash on delivery')))
    ordered_on = models.DateField(auto_now=True, verbose_name="Ordered On", null=True )
    paypal_transaction_id = models.CharField(max_length=10000000,verbose_name="Paypal Order Id", blank=True)
    delivered_on = models.DateField( verbose_name="Delivered On", null=True)
    payment_done = models.BooleanField(default=False, verbose_name='Payment Complete')
    completed = models.BooleanField(default=False, verbose_name='Order Status(Completionn)')

    def __str__(self):
        return
