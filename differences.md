1. Coroutine

    Définition : Une coroutine est une unité d'exécution légère qui permet de réaliser de la concurrence coopérative. Contrairement à un thread, une coroutine n'a pas besoin d'un système d'exploitation pour être gérée ; elle est souvent gérée par l'application elle-même ou par l'interpréteur (par exemple, dans Python).
    Mode d'exécution : Les coroutines sont des fonctions qui peuvent être suspendues et reprises. Elles s'exécutent dans un seul thread et ne permettent pas de véritable parallélisme. Elles fonctionnent selon un modèle "non bloquant", ce qui signifie qu'elles attendent volontairement qu'une autre coroutine prenne le relais (par exemple, lors d'opérations d'entrée/sortie).
    Exemple d'utilisation : Python asyncio et les fonctions async/await.
    Avantage : Faible coût en ressources car elles sont gérées au niveau du programme, avec peu de surcharge.

2. Thread

    Définition : Un thread est une unité d'exécution gérée par le système d'exploitation, qui permet de réaliser de la concurrence préemptive. Les threads d'un même processus partagent le même espace mémoire, ce qui facilite la communication entre eux.
    Mode d'exécution : Les threads peuvent s'exécuter en parallèle sur des cœurs de processeurs différents (sous réserve des capacités du processeur), ou être gérés de manière multitâche par le système. Le système d'exploitation interrompt les threads et détermine quand ils doivent être exécutés.
    Exemple d'utilisation : threading en Python ou std::thread en C++.
    Avantage : Permet l'exécution parallèle véritable sur plusieurs cœurs de processeur. Partager la mémoire entre threads est rapide, mais peut entraîner des problèmes de concurrence comme des conditions de course.

3. Processus

    Définition : Un processus est une instance indépendante d'un programme en cours d'exécution. Chaque processus a son propre espace mémoire et ne partage pas de données directement avec d'autres processus, à moins d'utiliser des mécanismes de communication inter-processus (IPC, inter-process communication).
    Mode d'exécution : Les processus peuvent également être exécutés en parallèle, chaque processus ayant son propre environnement d'exécution isolé. Les systèmes d'exploitation gèrent les processus et leur attribuent du temps d'exécution sur le CPU.
    Exemple d'utilisation : multiprocessing en Python ou la création de processus avec fork() en C.
    Avantage : Isolation complète entre les processus, ce qui garantit qu'un processus qui plante n'affecte pas les autres. Cependant, la communication entre processus est plus lente que celle entre threads.

Résumé des différences principales
Aspect	Coroutine	Thread	Processus
Gestion	Par le programme ou l'interpréteur	Par le système d'exploitation	Par le système d'exploitation
Concurrence/Parallélisme	Concurrence coopérative (non bloquante)	Concurrence préemptive, potentiel parallélisme	Parallélisme complet
Mémoire	Partagée (mais reste dans un seul thread)	Partagée entre threads d'un même processus	Isolée pour chaque processus
Coût en ressources	Faible	Modéré	Plus élevé (chaque processus est indépendant)
Exemple d'utilisation	asyncio en Python	threading en Python	multiprocessing en Python
Choix d'utilisation :

    Coroutine : Utilisée pour des tâches I/O intensives (comme les requêtes réseau) où le parallélisme CPU n'est pas nécessaire, mais où on veut éviter de bloquer l'application.
    Thread : Utile pour les tâches légères qui nécessitent du parallélisme et qui partagent beaucoup de données (par exemple, des tâches calculatoires modérées).
    Processus : Utilisé pour des tâches lourdes ou quand il est nécessaire d'isoler complètement l'exécution (par exemple, des tâches qui consomment beaucoup de CPU ou qui doivent être indépendantes).

    =====================
Le multiprocessing en Python est une méthode permettant d'exécuter des tâches en parallèle sur plusieurs CPU. Cette technique améliore les performances des programmes en distribuant les tâches sur différents processus. Chaque processus fonctionne de manière indépendante, réduisant ainsi le temps total d'exécution. Cependant, le coût de communication entre processus doit être inférieur au gain de performance pour justifier l'utilisation du multiprocessing.
====> https://docs.python.org/fr/3.7/library/multiprocessing.html
==============================

