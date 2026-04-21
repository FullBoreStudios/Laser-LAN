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


class HitSensorZone(models.TextChoices):
    HEAD = "head", "Head"
    TORSO = "torso", "Torso"
    BACK = "back", "Back"
    LEFT_ARM = "left_arm", "Left Arm"
    RIGHT_ARM = "right_arm", "Right Arm"
    LEFT_LEG = "left_leg", "Left Leg"
    RIGHT_LEG = "right_leg", "Right Leg"
    GEAR = "gear", "Gear"
    UNKNOWN = "unknown", "Unknown"


class HitResolutionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED_DUPLICATE = "rejected_duplicate", "Rejected Duplicate"
    REJECTED_FRIENDLY_FIRE = "rejected_friendly_fire", "Rejected Friendly Fire"
    REJECTED_ROUND_INACTIVE = "rejected_round_inactive", "Rejected Round Inactive"
    REJECTED_TARGET_DEAD = "rejected_target_dead", "Rejected Target Dead"
    REJECTED_UNKNOWN_SOURCE = "rejected_unknown_source", "Rejected Unknown Source"
    REJECTED_INVALID_PULSE = "rejected_invalid_pulse", "Rejected Invalid Pulse"


class FireResolutionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED_DUPLICATE = "rejected_duplicate", "Rejected Duplicate"
    REJECTED_ROUND_INACTIVE = "rejected_round_inactive", "Rejected Round Inactive"
    REJECTED_PLAYER_DEAD = "rejected_player_dead", "Rejected Player Dead"
    REJECTED_UNKNOWN_SOURCE = "rejected_unknown_source", "Rejected Unknown Source"
    REJECTED_NO_AMMO = "rejected_no_ammo", "Rejected No Ammo"
    REJECTED_INVALID_PAYLOAD = "rejected_invalid_payload", "Rejected Invalid Payload"


class Player(TimeStampedModel):
    display_name = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_name"]
        verbose_name = "player"
        verbose_name_plural = "players"

    def __str__(self):
        return self.display_name


class Team(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "team"
        verbose_name_plural = "teams"

    def __str__(self):
        return self.name


class TeamMembership(TimeStampedModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="team_memberships")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "team membership"
        verbose_name_plural = "team memberships"
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
        verbose_name = "arena"
        verbose_name_plural = "arenas"

    def __str__(self):
        return self.name


class BombSite(TimeStampedModel):
    arena = models.ForeignKey(Arena, on_delete=models.CASCADE, related_name="bomb_sites")
    code = models.CharField(max_length=16)
    label = models.CharField(max_length=32)

    class Meta:
        ordering = ["arena__name", "code"]
        verbose_name = "bomb site"
        verbose_name_plural = "bomb sites"
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
        verbose_name = "weapon"
        verbose_name_plural = "weapons"

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
        verbose_name = "match"
        verbose_name_plural = "matches"

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
        verbose_name = "match team"
        verbose_name_plural = "match teams"
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
        verbose_name = "match player"
        verbose_name_plural = "match players"
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
        verbose_name = "round"
        verbose_name_plural = "rounds"
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
    current_magazine_ammo = models.PositiveSmallIntegerField(default=0)
    current_reserve_ammo = models.PositiveSmallIntegerField(default=0)
    shots_fired = models.PositiveIntegerField(default=0)
    reload_count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["round_id", "match_player_id"]
        verbose_name = "round player state"
        verbose_name_plural = "round player states"
        constraints = [
            models.UniqueConstraint(
                fields=["round", "match_player"],
                name="unique_round_state_per_player",
            ),
        ]

    def __str__(self):
        return f"{self.match_player} state in {self.round}"


class FireEvent(TimeStampedModel):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="fire_events")
    sequence = models.PositiveIntegerField()
    occurred_at = models.DateTimeField()
    shooter = models.ForeignKey(
        MatchPlayer,
        on_delete=models.CASCADE,
        related_name="fire_events",
    )
    weapon = models.ForeignKey(
        Weapon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fire_events",
    )
    trigger_identifier = models.CharField(max_length=64, db_index=True)
    burst_size = models.PositiveSmallIntegerField(default=1)
    reporting_device_identifier = models.CharField(max_length=64, blank=True)
    source_device_identifier = models.CharField(max_length=64, blank=True)
    magazine_ammo_before = models.PositiveSmallIntegerField(default=0)
    magazine_ammo_after = models.PositiveSmallIntegerField(default=0)
    reserve_ammo_before = models.PositiveSmallIntegerField(default=0)
    reserve_ammo_after = models.PositiveSmallIntegerField(default=0)
    empty_trigger = models.BooleanField(default=False)
    requires_reload = models.BooleanField(default=False)
    resolution_status = models.CharField(
        max_length=32,
        choices=FireResolutionStatus.choices,
        default=FireResolutionStatus.PENDING,
    )
    resolution_notes = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["round_id", "sequence"]
        verbose_name = "fire event"
        verbose_name_plural = "fire events"
        constraints = [
            models.UniqueConstraint(fields=["round", "sequence"], name="unique_fire_sequence_per_round"),
        ]
        indexes = [
            models.Index(fields=["round", "occurred_at"], name="fireevent_round_time_idx"),
            models.Index(fields=["shooter", "occurred_at"], name="fireevent_shooter_time_idx"),
            models.Index(fields=["weapon", "occurred_at"], name="fireevent_weapon_time_idx"),
            models.Index(fields=["resolution_status"], name="fireevent_status_idx"),
        ]

    def __str__(self):
        return f"Fire event {self.sequence} in {self.round}"


class HitReport(TimeStampedModel):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="hit_reports")
    sequence = models.PositiveIntegerField()
    occurred_at = models.DateTimeField()
    victim = models.ForeignKey(
        MatchPlayer,
        on_delete=models.CASCADE,
        related_name="hit_reports_received",
    )
    attacker = models.ForeignKey(
        MatchPlayer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hit_reports_sent",
    )
    weapon = models.ForeignKey(
        Weapon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hit_reports",
    )
    pulse_identifier = models.CharField(max_length=64, db_index=True)
    shot_identifier = models.CharField(max_length=64, blank=True, db_index=True)
    reporting_device_identifier = models.CharField(max_length=64, blank=True)
    source_device_identifier = models.CharField(max_length=64, blank=True)
    sensor_code = models.CharField(max_length=32, blank=True)
    sensor_zone = models.CharField(
        max_length=16,
        choices=HitSensorZone.choices,
        default=HitSensorZone.UNKNOWN,
    )
    signal_strength = models.PositiveSmallIntegerField(null=True, blank=True)
    resolution_status = models.CharField(
        max_length=32,
        choices=HitResolutionStatus.choices,
        default=HitResolutionStatus.PENDING,
    )
    resolution_notes = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["round_id", "sequence"]
        verbose_name = "hit report"
        verbose_name_plural = "hit reports"
        constraints = [
            models.UniqueConstraint(fields=["round", "sequence"], name="unique_hit_sequence_per_round"),
        ]
        indexes = [
            models.Index(fields=["round", "occurred_at"], name="hitreport_round_time_idx"),
            models.Index(fields=["victim", "occurred_at"], name="hitreport_victim_time_idx"),
            models.Index(fields=["attacker", "occurred_at"], name="hitreport_attacker_time_idx"),
            models.Index(fields=["resolution_status"], name="hitreport_status_idx"),
        ]

    def __str__(self):
        return f"Hit report {self.sequence} in {self.round}"


class CombatEvent(TimeStampedModel):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="combat_events")
    sequence = models.PositiveIntegerField()
    occurred_at = models.DateTimeField()
    hit_report = models.OneToOneField(
        HitReport,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="combat_event",
    )
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
        verbose_name = "combat event"
        verbose_name_plural = "combat events"
        constraints = [
            models.UniqueConstraint(fields=["round", "sequence"], name="unique_combat_sequence_per_round"),
        ]
        indexes = [
            models.Index(fields=["round", "occurred_at"], name="combatevent_round_time_idx"),
            models.Index(fields=["victim", "occurred_at"], name="combatevent_victim_time_idx"),
            models.Index(fields=["attacker", "occurred_at"], name="combatevent_attacker_time_idx"),
            models.Index(fields=["weapon", "occurred_at"], name="combatevent_weapon_time_idx"),
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
        verbose_name = "bomb event"
        verbose_name_plural = "bomb events"
        constraints = [
            models.UniqueConstraint(fields=["round", "sequence"], name="unique_bomb_sequence_per_round"),
        ]

    def __str__(self):
        return f"{self.kind} in {self.round}"
