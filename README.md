# Vehicle-Routing-Problem-

Αυτή είναι μια ομαδική εργασία με τoυς @GrammatikakisDimitris , @sergiloupa, @marsidmali και @Giorgos Malandrakis στο μάθημα Μέθοδοι Βελτιστοποίησης στη Διοικητική Επιστήμη

Περιγραφή εργασίας

Στα πλαίσια της άσκησης θα επιλύσουμε ένα πρόβλημα δρομολόγησης οχημάτων, το οποίο σχετίζεται με την παροχή
βοήθειας-υλικών σε διάφορα γεωγραφικά σημεία μετά από φυσικές καταστροφές.
Το επιχειρησιακό σενάριο έχει ως εξής:
1. Μετά από μία μεγάλη φυσική καταστροφή, καλούμαστε να μεταφέρουμε όσο το δυνατό γρηγορότερα,
απαραίτητες προμήθειες σε ένα σύνολο 100 γεωγραφικών σημείων.
2. Κάθε γεωγραφικό σημείο καλύπτει διαφορετικά τμήματα του πληθυσμού, έτσι ώστε κάθε ένα από αυτά να έχει
διαφορετικές ανάγκες προμηθειών.
3. Για τη μεταφορά των προμηθειών χρησιμοποιείται ένας ομογενής στόλος οχημάτων τα οποία έχουν δεδομένη
χωρητικότητα προϊόντων.
4. Κάθε φορτηγό ξεκινά τη διαδρομή του από τη κεντρική αποθήκη 𝑑 = {0} και επισκέπτεται διαδοχικά κάποια
από τα 100 σημεία εξυπηρέτησης 𝑁 = {1,2,3, … , 100}
5. Οι διαδρομές όλων των φορτηγών ξεκινούν ταυτόχρονα
6. Κάθε σημείο εξυπηρέτησης ικανοποιείται από μία μόνο επίσκεψη ενός αποκλειστικά οχήματος. Επομένως, όταν
ένα όχημα επισκέπτεται ένα σημείο εξυπηρέτησης, παραδίδει σε αυτό το σύνολο των απαιτούμενων
προμηθειών.
7. Σε κάθε σημείο εξυπηρέτησης 𝑖 ∈ 𝑁, απαιτείται ένα χρονικό διάστημα για την εκφόρτωση των προμηθειών
Ο σχεδιασμός των διαδρομών πρέπει να ελαχιστοποιεί τον αθροιστικό χρόνο ολοκλήρωσης της παραλαβής των
προϊόντων από όλα τα σημεία.
