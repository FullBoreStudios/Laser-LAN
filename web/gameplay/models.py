from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TeamSide(models.TextChoices):
    TERRORISTS = "T", "Terrorists"
    COUNTER_TERRORISTS = "CT", "Counter-Terrorists"


class MatchStatus(models.TextChoices):
    STAGED = "staged", "Staged"
    LIVE = "live", "Live"
    COMPLETE = "complete", "Complete"
    CANCELLED = "cancelled", "Cancelled"


class GameMode(models.TextChoices):
    BOMB_DEFUSAL = "bomb_defusal", "Bomb Defusal"


class RoundStatus(models.TextChoices):
    PREPARING = "preparing", "Preparing"
    LIVE = "live", "Live"
    COMPLETE = "complete", "Complete"


class RoundWinReason(models.TextChoices):
    ELIMINATION = "elimination", "Elimination"
    BOMB_DEFUSED = "bomb_defused", "Bomb Defused"
    BOMB_DETONATED = "bomb_detonated", "Bomb Detonated"
    TIME_EXPIRED = "time_expired", "Time Expired"
    FORFEIT = "forfeit", "Forfeit"


class WeaponSlot(models.TextChoices):
    PRIMARY = "primary", "Primary"
    SECONDARY = "secondary", "Secondary"
    EQUIPMENT = "equipment", "Equipment"


class BombEventKind(models.TextChoices):
    PLANT_STARTED = "plant_started", "Plant Started"
    PLANTED = "planted", "Planted"
    DEFUSE_STARTED = "defuse_started", "Defuse Started"
    DEFUSE_CANCELLED = "defuse_cancelled", "Defuse Cancelled"
    DEFUSED = "defused", "Defused"
    DETONATED = "detonated", "Detonated"


class Player(TimeStampedModel):
    display_name = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_name"]

    def __str__(self):
        return self.display_name


class Team(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TeamMembership(TimeStampedModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="team_memberships")
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["team", "player"], name="unique_team_membership"),
        ]

    def __str__(self):
        return f"{self.player} on {self.team}"


class Arena(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)
    code = models.SlugField(max_length=32, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class BombSite(TimeStampedModel):
    arena = models.ForeignKey(Arena, on_delete=models.CASCADE, related_name="bomb_sites")
    code = models.CharField(max_length=16)
    label = models.CharField(max_length=32)

    class Meta:
        ordering = ["arena__name", "code"]
        constraints = [
            models.UniqueConstraint(fields=["arena", "code"], name="unique_bomb_site_per_arena"),
        ]

    def __str__(self):
        return f"{self.arena} {self.code}"


class Weapon(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)
    code = models.SlugField(max_length=32, unique=True)
    slot = models.CharField(max_length=16, choices=WeaponSlot.choices, default=WeaponSlot.PRIMARY)
    base_damage = models.PositiveSmallIntegerField()
    magazine_capacity = models.PositiveSmallIntegerField(default=30)
    reserve_ammo = models.PositiveSmallIntegerField(default=90)
    rounds_per_minute = models.PositiveSmallIntegerField(default=600)
    reload_time_ms = models.PositiveIntegerField(default=2500)
    effective_range_meters = models.DecimalField(max_digits=5, decimal_places=2, default=25)
    pellets_per_shot = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["slot", "name"]

    def __str__(self):
        return self.name


class Match(TimeStampedModel):
    mode = models.CharField(max_length=32, choices=GameMode.choices, default=GameMode.BOMB_DEFUSAL)
    arena = models.ForeignKey(
        Arena,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matches",
    )
    status = models.CharField(max_length=16, choices=MatchStatus.choices, default=MatchStatus.STAGED)
    team_size = models.PositiveSmallIntegerField(default=5)
    round_time_limit_seconds = models.PositiveSmallIntegerField(default=115)
    bomb_timer_seconds = models.PositiveSmallIntegerField(default=40)
    current_round_number = models.PositiveSmallIntegerField(default=0)
    winning_side = models.CharField(
        max_length=2,
        choices=TeamSide.choices,
        blank=True,
        null=True,
    )
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_mode_display()} match #{self.pk}"


class MatchTeam(TimeStampedModel):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="teams")
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="match_entries",
    )
    side = models.CharField(max_length=2, choices=TeamSide.choices)
    display_name = models.CharField(max_length=64)
    score = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["match_id", "side"]
        constraints = [
            models.UniqueConstraint(fields=["match", "side"], name="unique_match_side"),
        ]

    def __str__(self):
        return f"{self.match} {self.get_side_display()}"


class MatchPlayer(TimeStampedModel):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="players")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="match_entries")
    match_team = models.ForeignKey(MatchTeam, on_delete=models.CASCADE, related_name="players")
    selected_weapon = models.ForeignKey(
        Weapon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="selected_by_players",
    )
    phone_identifier = models.CharField(max_length=64, blank=True)
    gun_identifier = models.CharField(max_length=64, blank=True)
    vest_identifier = models.CharField(max_length=64, blank=True)
    is_connected = models.BooleanField(default=False)
    is_ready = models.BooleanField(default=False)

    class Meta:
        ordering = ["match_id", "player__display_name"]
        constraints = [
            models.UniqueConstraint(fields=["match", "player"], name="unique_player_per_match"),
        ]

    def __str__(self):
        return f"{self.player} in {self.match}"


class Round(TimeStampedModel):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="rounds")
    number = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=16, choices=RoundStatus.choices, default=RoundStatus.PREPARING)
    winning_side = models.CharField(
        max_length=2,
        choices=TeamSide.choices,
        blank=True,
        null=True,
    )
    win_reason = models.CharField(
        max_length=32,
        choices=RoundWinReason.choices,
        blank=True,
        null=True,
    )
    planted_site = models.ForeignKey(
        BombSite,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="planted_rounds",
    )
    bomb_planted_by = models.ForeignKey(
        MatchPlayer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bomb_plants",
    )
    bomb_defused_by = models.ForeignKey(
        MatchPlayer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bomb_defuses",
    )
    bomb_planted_at = models.DateTimeField(blank=True, null=True)
    bomb_defused_at = models.DateTimeField(blank=True, null=True)
    bomb_detonated_at = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["match_id", "number"]
        constraints = [
            models.UniqueConstraint(fields=["match", "number"], name="unique_round_number_per_match"),
        ]

    def __str__(self):
        return f"{self.match} round {self.number}"


class RoundPlayerState(TimeStampedModel):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="player_states")
    match_player = models.ForeignKey(
        MatchPlayer,
        on_delete=models.CASCADE,
        related_name="round_states",
    )
    starting_health = models.PositiveSmallIntegerField(default=100)
    current_health = models.PositiveSmallIntegerField(default=100)
    alive = models.BooleanField(default=True)
    deaths = models.PositiveSmallIntegerField(default=0)
    equipped_weapon = models.ForeignKey(
        Weapon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="equipped_in_round_states",
    )

    class Meta:
        ordering = ["round_id", "match_player_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["round", "match_player"],
                name="unique_round_state_per_player",
            ),
        ]

    def __str__(self):
        return f"{self.match_player} state in {self.round}"


class CombatEvent(TimeStampedModel):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="combat_events")
    sequence = models.PositiveIntegerField()
    occurred_at = models.DateTimeField()
    attacker = models.ForeignKey(
        MatchPlayer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="damage_dealt_events",
    )
    victim = models.ForeignKey(
        MatchPlayer,
        on_delete=models.CASCADE,
        related_name="damage_taken_events",
    )
    weapon = models.ForeignKey(
        Weapon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="combat_events",
    )
    damage = models.PositiveSmallIntegerField()
    victim_health_after = models.PositiveSmallIntegerField()
    was_lethal = models.BooleanField(default=False)

    class Meta:
        ordering = ["round_id", "sequence"]
        constraints = [
            models.UniqueConstraint(fields=["round", "sequence"], name="unique_combat_sequence_per_round"),
        ]

    def __str__(self):
        return f"Combat event {self.sequence} in {self.round}"


class BombEvent(TimeStampedModel):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="bomb_events")
    sequence = models.PositiveIntegerField()
    occurred_at = models.DateTimeField()
    kind = models.CharField(max_length=32, choices=BombEventKind.choices)
    actor = models.ForeignKey(
        MatchPlayer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bomb_events",
    )
    site = models.ForeignKey(
        BombSite,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bomb_events",
    )

    class Meta:
        ordering = ["round_id", "sequence"]
        constraints = [
            models.UniqueConstraint(fields=["round", "sequence"], name="unique_bomb_sequence_per_round"),
        ]

    def __str__(self):
        return f"{self.kind} in {self.round}"
